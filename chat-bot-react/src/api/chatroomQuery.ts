import { apiRequest } from "./httpService";
import type { ChatRoom } from "../model/chatroom";

export const getChatrooms = async () => {
  return apiRequest<ChatRoom[]>("get", "/chatRooms");
};

export const createNewChatroom = async (chatroomName: string) => {
  return apiRequest<ChatRoom>("post", "/chatRooms", { name: chatroomName });
};

export const deleteChatroom = async (chatroomId: string) => {
  return apiRequest<void>("delete", `/chatRooms/${chatroomId}`);
};
