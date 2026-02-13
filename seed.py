import random
from datetime import datetime, timedelta
from faker import Faker
from app.database import SessionLocal, engine
from app import models, crud
from sqlalchemy.orm import Session

# Initialize Faker
fake = Faker()

def seed_data():
    db = SessionLocal()
    
    try:
        # Create user
        user_email = "test@example.com"
        user = crud.get_user_by_email(db, email=user_email)
        
        if not user:
            print(f"Creating user {user_email}...")
            hashed_password = crud.get_password_hash("password123")
            user = models.User(
                email=user_email,
                password=hashed_password,
                first_name="Test",
                last_name="User"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            print(f"User {user_email} already exists.")
            
        user_id = user.id
        
        # Create Categories
        categories = [
            "Food", "Transport", "Utilities", "Entertainment", 
            "Shopping", "Health", "Rent", "Groceries", "Dining Out", "Travel"
        ]
        
        db_categories = []
        existing_categories = db.query(models.Category).filter(models.Category.user_id == user_id).all()
        existing_names = [c.category_name for c in existing_categories]
        
        print("Seeding categories...")
        for cat_name in categories:
            if cat_name not in existing_names:
                cat = models.Category(
                    category_name=cat_name,
                    user_id=user_id,
                    is_deleted=False
                )
                db.add(cat)
                db_categories.append(cat)
        
        db.commit()
        # Refresh to get IDs
        all_categories = db.query(models.Category).filter(models.Category.user_id == user_id).all()
        
        if not all_categories:
            print("No categories found/created. Aborting spending seed.")
            return

        # Time range: past 3 months (90 days)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=90)
        
        print("Seeding income...")
        # 1. Monthly Salary (3 times)
        current_date_month = start_date
        while current_date_month < end_date:
            salary_date = current_date_month.replace(day=28) # Payday 28th
            if salary_date > end_date:
                break
                
            # Check if salary already exists for this month roughly
            existing_salary = db.query(models.Income).filter(
                models.Income.user_id == user_id,
                models.Income.source == "Salary",
                models.Income.date >= salary_date - timedelta(days=2),
                models.Income.date <= salary_date + timedelta(days=2)
            ).first()
            
            if not existing_salary:
                salary = models.Income(
                    amount=5000.0,
                    source="Salary",
                    date=salary_date,
                    user_id=user_id,
                    type="transaction", # Assuming 'transaction' or check schema
                    currency=models.Currency.NGN
                )
                db.add(salary)
            
            # Next month 
            if current_date_month.month == 12:
                current_date_month = current_date_month.replace(year=current_date_month.year + 1, month=1)
            else:
                current_date_month = current_date_month.replace(month=current_date_month.month + 1)
        
        # 2. Random Incomes (Freelance, Gift, etc)
        for _ in range(5):
            date = fake.date_time_between(start_date=start_date, end_date=end_date)
            income_amount = round(random.uniform(100.0, 1500.0), 2)
            income = models.Income(
                amount=income_amount,
                source=random.choice(["Freelance", "Gift", "Bonus", "Dividend"]),
                date=date,
                user_id=user_id,
                type="transaction",
                currency=models.Currency.NGN
            )
            db.add(income)
            
        db.commit()

        print("Seeding spending...")
        # Generate random spending
        for _ in range(50): # 50 transactions over 90 days
            date = fake.date_time_between(start_date=start_date, end_date=end_date)
            amount = round(random.uniform(10.0, 300.0), 2)
            category = random.choice(all_categories)
            item_name = fake.word().capitalize()
            
            spending = models.Spending(
                amount=amount,
                notes=fake.sentence(),
                item_name=item_name,
                date=date,
                user_id=user_id,
                category_id=category.id,
                is_deleted=False,
                currency=models.Currency.NGN
            )
            db.add(spending)
            
        db.commit()
        
        print("Seeding savings goals...")
        goals = [
            ("New Laptop", 2000.0),
            ("Vacation", 5000.0),
            ("Emergency Fund", 10000.0)
        ]
        
        db_goals = []
        for name, target in goals:
            existing_goal = db.query(models.SavingsGoal).filter(
                models.SavingsGoal.user_id == user_id, 
                models.SavingsGoal.goal_name == name
            ).first()
            
            if not existing_goal:
                goal = models.SavingsGoal(
                    goal_name=name,
                    target_amount=target,
                    deadline=fake.date_time_between(start_date=end_date, end_date=end_date + timedelta(days=180)),
                    user_id=user_id,
                    created_at=start_date,
                    currency=models.Currency.NGN
                )
                db.add(goal)
                db.flush() # flush to get ID
                db_goals.append(goal)
            else:
                db_goals.append(existing_goal)
                
        db.commit()
        
        print("Seeding savings contributions...")
        for goal in db_goals:
            # Add 3-5 contributions per goal
            for _ in range(random.randint(3, 5)):
                amount = round(random.uniform(50.0, 500.0), 2)
                date = fake.date_time_between(start_date=start_date, end_date=end_date)
                
                contribution = models.SavingsContribution(
                    amount=amount,
                    date=date,
                    goal_id=goal.id,
                    user_id=user_id,
                    currency=models.Currency.NGN
                )
                db.add(contribution)
                
        db.commit()
        
        print("Database seeded successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
