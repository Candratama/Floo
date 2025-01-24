import axios from "axios";
import {
  Category,
  CategoryCreateInput,
  CategoryUpdateInput,
} from "@/types/category";

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

export async function getCategories(): Promise<Category[]> {
  const endpoint = "/categories/";
  const url = `${API_URL}${endpoint}`;
  const token = localStorage.getItem("token");

  console.log("=== Category API Request ===");
  console.log("URL:", url);
  console.log("Method: GET");
  console.log("Headers:", {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "No token",
  });

  try {
    const response = await api.get<Category[]>(endpoint);
    console.log("=== Category API Response ===");
    console.log("Status:", response.status);
    console.log("Status Text:", response.statusText);
    console.log("Data:", response.data);
    return response.data;
  } catch (error) {
    console.log("=== Category API Error ===");
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

export async function createCategory(
  name: string,
  is_income: boolean
): Promise<Category> {
  const endpoint = "/categories/";
  const url = `${API_URL}${endpoint}`;
  const token = localStorage.getItem("token");
  const input: CategoryCreateInput = {
    name,
    is_income,
  };

  console.log("=== Create Category API Request ===");
  console.log("URL:", url);
  console.log("Method: POST");
  console.log("Headers:", {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "No token",
  });
  console.log("Body:", input);

  try {
    const response = await api.post<Category>(endpoint, input);
    console.log("=== Create Category API Response ===");
    console.log("Status:", response.status);
    console.log("Status Text:", response.statusText);
    console.log("Data:", response.data);
    return response.data;
  } catch (error) {
    console.log("=== Create Category API Error ===");
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

export async function updateCategory(
  id: number,
  name: string,
  is_income: boolean
): Promise<Category> {
  const endpoint = `/categories/${id}`;
  const url = `${API_URL}${endpoint}`;
  const token = localStorage.getItem("token");
  const input: CategoryUpdateInput = {
    name,
    is_income,
  };

  console.log("=== Update Category API Request ===");
  console.log("URL:", url);
  console.log("Method: PATCH");
  console.log("Headers:", {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "No token",
  });
  console.log("Body:", input);

  try {
    const response = await api.patch<Category>(endpoint, input);
    console.log("=== Update Category API Response ===");
    console.log("Status:", response.status);
    console.log("Status Text:", response.statusText);
    console.log("Data:", response.data);
    return response.data;
  } catch (error) {
    console.log("=== Update Category API Error ===");
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

export async function deleteCategory(id: number): Promise<void> {
  const endpoint = `/categories/${id}`;
  const url = `${API_URL}${endpoint}`;
  const token = localStorage.getItem("token");

  console.log("=== Delete Category API Request ===");
  console.log("URL:", url);
  console.log("Method: DELETE");
  console.log("Headers:", {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "No token",
  });

  try {
    const response = await api.delete(endpoint);
    console.log("=== Delete Category API Response ===");
    console.log("Status:", response.status);
    console.log("Status Text:", response.statusText);
  } catch (error) {
    console.log("=== Delete Category API Error ===");
    const apiError = error as ApiErrorResponse;

    // Check if the error is due to transactions linked to the category
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

    throw new Error("Failed to delete category. Please try again later.");
  }
}
