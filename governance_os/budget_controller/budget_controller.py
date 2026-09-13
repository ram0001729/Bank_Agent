class BudgetController:
    """Cumulative agent spending limit controller."""
    def __init__(self, daily_budget_cap: float = 100000.0):
        self.daily_budget_cap = daily_budget_cap
        self.cumulative_spent = 0.0

    def check_and_reserve_budget(self, amount: float) -> bool:
        if self.cumulative_spent + amount > self.daily_budget_cap:
            return False
        self.cumulative_spent += amount
        return True
