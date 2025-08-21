// config/environment.ts - Environment configuration
interface Environment {
  API_BASE_URL: string;
  ENVIRONMENT: "development" | "production";
}

const getEnvironment = (): Environment => {
  // Check if we're in development or production
  const isDevelopment =
    import.meta.env.DEV || window.location.hostname === "localhost";

  if (isDevelopment) {
    return {
      API_BASE_URL: "http://localhost:5000/api",
      ENVIRONMENT: "development",
    };
  } else {
    return {
      API_BASE_URL: "https://mandyy1223.pythonanywhere.com/api",
      ENVIRONMENT: "production",
    };
  }
};

export const config = getEnvironment();
export default config;
