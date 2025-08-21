import { apiRequest } from "./httpService";
import type { Message } from "../model/message";

export const getMessages = async (chatroomId: string) => {
  return apiRequest<Message[]>("get", `/chatRooms/${chatroomId}/messages`);
};

export const sendMessage = async (
  chatroomId: string,
  text: string,
  file: File | null
): Promise<Message> => {
  const formData = new FormData();
  formData.append("chatroom_id", chatroomId);
  formData.append("sender", "user");
  if (text) {
    formData.append("text", text);
  }
  if (file) {
    formData.append("file", file);
  }

  return apiRequest<Message>("post", "/messages/gemini", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

export const editMessage = async (
  messageId: string,
  newText: string
): Promise<Message> => {
  return apiRequest<Message>("put", `/messages/${messageId}`, {
    text: newText,
  });
};
