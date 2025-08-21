import React from "react";
import {
  List,
  Typography,
  Box,
  Button,
  TextField,
  IconButton,
  Tooltip,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import SaveIcon from "@mui/icons-material/Save";
import CancelIcon from "@mui/icons-material/Cancel";
import { StyledMessage, MessageBubble } from "../styles/MessageStyles";
import { getImageUrl } from "../utils/imageUtils";
import type { Message } from "../model/message";

interface MessageListProps {
  messages: Message[] | undefined;
  isLoadingMessages: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
  editingMessageId: string | null;
  editText: string;
  setEditText: (text: string) => void;
  startEditingMessage: (messageId: string, currentText: string) => void;
  cancelEditingMessage: () => void;
  saveEditedMessage: () => void;
}

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  isLoadingMessages,
  messagesEndRef,
  editingMessageId,
  editText,
  setEditText,
  startEditingMessage,
  cancelEditingMessage,
  saveEditedMessage,
}) => {
  return (
    <List
      sx={{
        width: "100%",
        maxWidth: 800,
        bgcolor: "background.paper",
        border: "1px solid #ccc",
        borderRadius: "5px",
        padding: "10px",
        height: "400px",
        overflowY: "scroll",
        marginBottom: "20px",
      }}
    >
      {isLoadingMessages ? (
        <Button loading variant="text" />
      ) : (
        Array.isArray(messages) &&
        messages.map((message: Message) => (
          <StyledMessage key={message.id} sender={message.sender}>
            <MessageBubble sender={message.sender}>
              <Box
                sx={{
                  display: "flex",
                  alignItems: "center",
                  gap: 1,
                  width: "100%",
                }}
              >
                <Box sx={{ flex: 1 }}>
                  {editingMessageId === message.id ? (
                    <Box
                      sx={{
                        display: "flex",
                        flexDirection: "column",
                        gap: 1,
                      }}
                    >
                      <TextField
                        value={editText}
                        onChange={(e) => setEditText(e.target.value)}
                        multiline
                        maxRows={4}
                        fullWidth
                        variant="outlined"
                        size="small"
                        autoFocus
                        InputProps={{
                          style: { color: "#fff" },
                        }}
                        sx={{
                          "& .MuiOutlinedInput-root": {
                            color: "#fff",
                            "&:hover fieldset": {
                              borderColor: "#fff",
                            },
                            "&.Mui-focused fieldset": {
                              borderColor: "#fff",
                              borderWidth: "2px",
                            },
                          },
                          "& .MuiInputBase-input": {
                            color: "#fff",
                          },
                        }}
                      />
                      <Box sx={{ display: "flex", gap: 1 }}>
                        <Tooltip title="Save">
                          <IconButton
                            onClick={saveEditedMessage}
                            size="small"
                            sx={{
                              color: "#fff",
                              "&:hover": {
                                backgroundColor: "rgba(76, 175, 80, 0.1)",
                              },
                            }}
                          >
                            <SaveIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Cancel">
                          <IconButton
                            onClick={cancelEditingMessage}
                            size="small"
                            sx={{
                              color: "#fff",
                              "&:hover": {
                                backgroundColor: "rgba(117, 117, 117, 0.1)",
                              },
                            }}
                          >
                            <CancelIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </Box>
                    </Box>
                  ) : (
                    message.text && (
                      <Typography
                        variant="body1"
                        dangerouslySetInnerHTML={{ __html: message.text }}
                      />
                    )
                  )}
                  {message.image && getImageUrl(message.image) && (
                    <Box
                      component="img"
                      src={getImageUrl(message.image)!}
                      alt="Uploaded"
                      sx={{ maxWidth: "200px", maxHeight: "200px", mt: 1 }}
                    />
                  )}
                </Box>
                {!editingMessageId &&
                  message.sender === "user" &&
                  message.text && (
                    <Tooltip title="Edit message">
                      <IconButton
                        onClick={() =>
                          startEditingMessage(message.id, message.text || "")
                        }
                        size="small"
                        sx={{
                          color: "#ffffffff",
                          opacity: 0.7,
                          "&:hover": { opacity: 1 },
                          minWidth: "auto",
                        }}
                      >
                        <EditIcon
                          fontSize="small"
                          sx={{ color: "#ffffffff" }}
                        />
                      </IconButton>
                    </Tooltip>
                  )}
              </Box>
            </MessageBubble>
          </StyledMessage>
        ))
      )}
      <div ref={messagesEndRef} />
    </List>
  );
};
