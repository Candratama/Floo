import axios from "axios";
import { Bank, BankCreateInput, BankUpdateInput } from "@/types/bank";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface ApiErrorResponse {
  response?: {
    status: number;
    statusText: string;
    data: {
      detail?: string;
      message?: string;
    };
  };
  config?: {
    url?: string;
    method?: string;
    headers?: Record<string, string>;
    data?: string;
  };
  message?: string;
}

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle unauthorized responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401) {
      console.log("Unauthorized - Redirecting to login");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export async function getBanks(): Promise<Bank[]> {
  const endpoint = "/banks/";
  const url = `${API_URL}${endpoint}`;
  const token = localStorage.getItem("token");

  console.log("=== Bank API Request ===");
  console.log("URL:", url);
  console.log("Method: GET");
  console.log("Headers:", {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "No token",
  });

  try {
    const response = await api.get<Bank[]>(endpoint);
    console.log("=== Bank API Response ===");
    console.log("Status:", response.status);
    console.log("Status Text:", response.statusText);
    console.log("Data:", response.data);
    return response.data;
  } catch (error) {
    console.log("=== Bank API Error ===");
    const apiError = error as ApiErrorResponse;
    if (apiError.response) {
      console.log("Error Status:", apiError.response.status);
      console.log("Error Status Text:", apiError.response.statusText);
      console.log("Error Data:", apiError.response.data);
      console.log("Error Config:", {
        url: apiError.config?.url,
        method: apiError.config?.method,
        headers: apiError.config?.headers,
      });
    } else {
      console.log("Error:", apiError.message || "Unknown error");
    }
    throw error;
  }
}

export async function createBank(
  name: string,
  color: string,
  start_balance: number
): Promise<Bank> {
  const endpoint = "/banks/";
  const url = `${API_URL}${endpoint}`;
  const token = localStorage.getItem("token");
  const input: BankCreateInput = {
    name,
    color,
    start_balance,
  };

  console.log("=== Create Bank API Request ===");
  console.log("URL:", url);
  console.log("Method: POST");
  console.log("Headers:", {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "No token",
  });
  console.log("Body:", input);

  try {
    const response = await api.post<Bank>(endpoint, input);
    console.log("=== Create Bank API Response ===");
    console.log("Status:", response.status);
    console.log("Status Text:", response.statusText);
    console.log("Data:", response.data);
    return response.data;
  } catch (error) {
    console.log("=== Create Bank API Error ===");
    const apiError = error as ApiErrorResponse;
    if (apiError.response) {
      console.log("Error Status:", apiError.response.status);
      console.log("Error Status Text:", apiError.response.statusText);
      console.log("Error Data:", apiError.response.data);
      console.log("Error Config:", {
        url: apiError.config?.url,
        method: apiError.config?.method,
        headers: apiError.config?.headers,
        data: apiError.config?.data,
      });
    } else {
      console.log("Error:", apiError.message || "Unknown error");
    }
    throw error;
  }
}

export async function updateBank(
  id: number,
  name: string,
  color: string,
  start_balance: number
): Promise<Bank> {
  const endpoint = `/banks/${id}`;
  const url = `${API_URL}${endpoint}`;
  const token = localStorage.getItem("token");
  const input: BankUpdateInput = {
    name,
    color,
    start_balance,
  };

  console.log("=== Update Bank API Request ===");
  console.log("URL:", url);
  console.log("Method: PATCH");
  console.log("Headers:", {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "No token",
  });
  console.log("Body:", input);

  try {
    const response = await api.patch<Bank>(endpoint, input);
    console.log("=== Update Bank API Response ===");
    console.log("Status:", response.status);
    console.log("Status Text:", response.statusText);
    console.log("Data:", response.data);
    return response.data;
  } catch (error) {
    console.log("=== Update Bank API Error ===");
    const apiError = error as ApiErrorResponse;
    if (apiError.response) {
      console.log("Error Status:", apiError.response.status);
      console.log("Error Status Text:", apiError.response.statusText);
      console.log("Error Data:", apiError.response.data);
      console.log("Error Config:", {
        url: apiError.config?.url,
        method: apiError.config?.method,
        headers: apiError.config?.headers,
        data: apiError.config?.data,
      });
    } else {
      console.log("Error:", apiError.message || "Unknown error");
    }
    throw error;
  }
}

export async function deleteBank(id: number): Promise<void> {
  const endpoint = `/banks/${id}`;
  const url = `${API_URL}${endpoint}`;
  const token = localStorage.getItem("token");

  console.log("=== Delete Bank API Request ===");
  console.log("URL:", url);
  console.log("Method: DELETE");
  console.log("Headers:", {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "No token",
  });

  try {
    const response = await api.delete(endpoint);
    console.log("=== Delete Bank API Response ===");
    console.log("Status:", response.status);
    console.log("Status Text:", response.statusText);
  } catch (error) {
    console.log("=== Delete Bank API Error ===");
    const apiError = error as ApiErrorResponse;

    // Check if the error is due to transactions linked to the bank
    if (apiError.response?.status === 400 && apiError.response.data?.detail) {
      throw new Error(apiError.response.data.detail);
    }

    console.log("Error Status:", apiError.response?.status);
    console.log("Error Status Text:", apiError.response?.statusText);
    console.log("Error Data:", apiError.response?.data);
    console.log("Error Config:", {
      url: apiError.config?.url,
      method: apiError.config?.method,
      headers: apiError.config?.headers,
    });

    throw new Error("Failed to delete bank. Please try again later.");
  }
}
