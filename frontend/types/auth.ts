// types/auth.ts
export interface User {
  id: number;
  username: string;
  fullname: string;
  email: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterCredentials {
  fullname: string;
  username: string;
  email: string;
  password: string;
}
