from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import TimeConfig
from schemas import TimeConfigOut, TimeConfigUpdate
from routers.auth import verify_token

router = APIRouter(prefix="/api/timeconfig", tags=["TimeConfig"], dependencies=[Depends(verify_token)])


def _get_or_create(db: Session) -> TimeConfig:
    """Yagona (id=1) sozlama qatorini olish, bo'lmasa default bilan yaratish."""
    cfg = db.get(TimeConfig, 1)
    if not cfg:
        cfg = TimeConfig(id=1)
        db.add(cfg)
        db.commit()
        db.refresh(cfg)
    return cfg


@router.get("", response_model=TimeConfigOut)
def get_config(db: Session = Depends(get_db)):
    """
    Maktab vaqt sozlamalarini olish (smena soatlari, kunlar, tushlik chegarasi).

    **Qaytaradi:**
    - days_count: haftada o'quv kunlari (default 6)
    - shift1_periods: 1-smena soatlari soni
    - shift2_periods: 2-smena soatlari soni
    - morning_until: tushlikkacha hisoblanadigan soat chegarasi
    """
    return _get_or_create(db)


@router.put("", response_model=TimeConfigOut)
def update_config(data: TimeConfigUpdate, db: Session = Depends(get_db)):
    """
    Maktab vaqt sozlamalarini yangilash.

    **Parametrlar:**
    - days_count: haftada o'quv kunlari (1-6)
    - shift1_periods: 1-smena soatlari soni
    - shift2_periods: 2-smena soatlari soni
    - morning_until: tushlikkacha soat chegarasi (og'ir fanlar shu soatgacha afzal)
    """
    cfg = _get_or_create(db)
    cfg.days_count     = data.days_count
    cfg.shift1_periods = data.shift1_periods
    cfg.shift2_periods = data.shift2_periods
    cfg.morning_until  = data.morning_until
    db.commit()
    db.refresh(cfg)
    return cfg