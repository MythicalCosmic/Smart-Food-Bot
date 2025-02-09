from database.database import User, SessionLocal

def add_user(telegram_id, username, name, step):
    session = SessionLocal()
    existing_user = session.query(User).filter_by(telegram_id=telegram_id).first()
    
    if not existing_user:
        new_user = User(
            telegram_id=telegram_id,
            username=username,
            name=name,
            step=step
        )
        session.add(new_user)
        session.commit()
        session.close()
        return True
    session.close()
    return False