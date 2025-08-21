// httpService_production.ts - Production configuration
import axios from "axios";
import type {
  AxiosInstance,
  AxiosResponse,
  AxiosError,
  AxiosRequestConfig,
} from "axios";

// Production API URL for PythonAnywhere
const API_BASE_URL = "https://mandyy1223.pythonanywhere.com/api";

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // Increased timeout for production
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(
      `Making ${config.method?.toUpperCase()} request to ${config.url}`
    );
    return config;
  },
  (error: AxiosError) => {
    console.error("Request error:", error);
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log(`Response from ${response.config.url}:`, response.status);
    return response;
  },
  (error: AxiosError) => {
    console.error("Response error:", error.response?.data || error.message);

    if (error.response?.status === 401) {
      console.error("Unauthorized access");
    } else if (error.response?.status === 404) {
      console.error("Resource not found");
    } else if ((error.response?.status ?? 0) >= 500) {
      console.error("Server error");
    }

    return Promise.reject(error);
  }
);

export const apiRequest = async <T>(
  method: "get" | "post" | "put" | "delete",
  url: string,
  data?: unknown,
  config?: AxiosRequestConfig
): Promise<T> => {
  try {
    const response: AxiosResponse<T> = await apiClient({
      method,
      url,
      data,
      ...config,
    });
    return response.data;
  } catch (error) {
    console.error(`API request failed: ${method.toUpperCase()} ${url}`, error);
    throw error;
  }
};

export { apiClient };
export default apiClient;
