from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gym_database import Database 

app = FastAPI()
db = Database()

# --- DATA MODELS (Veri Modelleri) ---
class MemberModel(BaseModel):
    name: str
    balance: float  

class ActivityModel(BaseModel):
    member_id: int
    action: str # "Check-in" or "Check-out"

# --- ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "Welcome to the Gym Management System API 🏋️‍♂️"}

# 1. Add New Member
@app.post("/members")
def add_member(member: MemberModel):
    new_id = db.add_member(member.name, member.balance)
    return {
        "status": "Success", 
        "member_id": new_id, 
        "data": member
    }

# 2. List All Members
@app.get("/members")
def get_all_members():
    members_list = db.get_members()
    return {"total_count": len(members_list), "members": members_list}

# 3. Delete Member
@app.delete("/members/{member_id}")
def delete_member(member_id: int):
    db.delete_member(member_id)
    return {"status": "Deleted", "message": f"Member {member_id} removed successfully."}

# 4. Admin Reports
@app.get("/reports")
def get_reports():
    count, revenue = db.get_statistics()
    return {
        "active_members": count, 
        "total_balance_pool": revenue,
        "system_status": "Online 🟢"
    }

# --- ACCESS CONTROL SYSTEM (Turnike) ---
@app.post("/access")
def process_access(activity: ActivityModel):
    ENTRY_FEE = 50  # Cost per entry
    
    # Step 1: Find the member
    member = db.get_member_by_id(activity.member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    # DB returns: (id, name, balance) -> Index 2 is balance
    current_balance = member[2] 

    # Step 2: Check Logic (If entering, deduct money)
    if activity.action == "Check-in":
        
        # Check if balance is sufficient
        if current_balance < ENTRY_FEE:
            return {
                "status": "Denied ⛔", 
                "message": "Insufficient balance.", 
                "required": ENTRY_FEE,
                "current_balance": current_balance
            }
        
        # Deduct fee
        new_balance = current_balance - ENTRY_FEE
        db.update_balance(activity.member_id, new_balance)
        response_message = f"Access Granted. ${ENTRY_FEE} deducted."
    
    else:
        # If Check-out (Exit), just log it
        response_message = "Exit recorded. See you next time!"
        new_balance = current_balance

    # Step 3: Log the activity
    db.add_activity(activity.member_id, activity.action)
    
    return {
        "status": "Success ✅", 
        "message": response_message, 
        "remaining_balance": new_balance
    }