export interface Bank {
  id: number;
  name: string;
  user_id: number;
  color: string;
  start_balance: number;
  end_balance: number;
  created_at: string;
  updated_at: string;
}

export interface BankCreateInput {
  name: string;
  color: string;
  start_balance: number;
}

export interface BankUpdateInput {
  name: string;
  color: string;
  start_balance: number;
}
