import axios from "axios";
import type {
  AxiosInstance,
  AxiosResponse,
  AxiosError,
  AxiosRequestConfig,
} from "axios";
import { config } from "../config/environment";

const API_BASE_URL = config.API_BASE_URL;

// Create a reusable Axios instance
const httpService: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Define a type for the expected API response data
type ApiResponse<T> = T; // Or refine this if your API has a specific envelope
type dataType = unknown; // Adjust this type based on your API response structure

// Generic function to make API requests
export const apiRequest = async <T>(
  method: "get" | "post" | "put" | "delete",
  url: string,
  data?: dataType, // Keep `any` for request data as it varies widely
  config?: AxiosRequestConfig // Use AxiosRequestConfig for config
): Promise<ApiResponse<T>> => {
  try {
    let response: AxiosResponse<ApiResponse<T>>;

    switch (method) {
      case "get":
        response = await httpService.get<ApiResponse<T>>(url, config);
        break;
      case "post":
        response = await httpService.post<ApiResponse<T>>(url, data, config);
        break;
      case "put":
        response = await httpService.put<ApiResponse<T>>(url, data, config);
        break;
      case "delete":
        response = await httpService.delete<ApiResponse<T>>(url, config);
        break;
      default:
        throw new Error(`Unsupported HTTP method: ${method}`);
    }

    return response.data;
  } catch (error: unknown) {
    // Type the error as AxiosError if it's an Axios error
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError;
      console.error("Axios API Request Error:", axiosError.message); // Access specific error message
      throw axiosError; // Re-throw for component-level handling
    } else {
      // Handle non-Axios errors (e.g., network errors)
      console.error("API Request Error:", error);
      throw error;
    }
  }
};
