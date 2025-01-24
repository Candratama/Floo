export interface Category {
  id: number;
  name: string;
  is_income: boolean;
  created_at: string;
  updated_at: string;
}

export interface CategoryCreateInput {
  name: string;
  is_income: boolean;
}

export interface CategoryUpdateInput {
  name?: string;
  is_income?: boolean;
}
