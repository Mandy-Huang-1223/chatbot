// utils/imageUtils.ts - Image URL utilities for production
import { config } from "../config/environment";

const getBaseUrl = () => {
  if (config.ENVIRONMENT === "development") {
    return "http://localhost:5000";
  } else {
    return "https://mandyy1223.pythonanywhere.com";
  }
};

export const getImageUrl = (imagePath: string | null): string | null => {
  if (!imagePath) return null;

  // If it's already a full URL, return as is
  if (imagePath.startsWith("http")) {
    return imagePath;
  }

  // If it's a relative path, prepend the API base URL
  return `${getBaseUrl()}/uploads/${imagePath}`;
};

export const isValidImageUrl = (url: string | null): boolean => {
  if (!url) return false;
  return url.includes("/uploads/") || url.startsWith("blob:");
};
