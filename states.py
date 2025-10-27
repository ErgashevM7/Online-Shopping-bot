from aiogram.fsm.state import State, StatesGroup

class ProductStates(StatesGroup):
    selecting = State()
    choosing_amount = State()

class Karzinka(StatesGroup):
    contact = State()
    manzil = State()
    tasdiqlash = State()
