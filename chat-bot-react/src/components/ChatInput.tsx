import {
  Box,
  IconButton,
  TextField,
  Button,
  Typography,
  CircularProgress,
} from "@mui/material";
import { PhotoCamera, Close } from "@mui/icons-material";
import { useRef } from "react";

export const ChatInput = ({
  newMessage,
  setNewMessage,
  sendMessage,
  handleImageChange,
  isMessageSending,
  isImageUploading,
  selectedImage,
  onRemoveImage,
}: {
  newMessage: string;
  setNewMessage: (message: string) => void;
  sendMessage: () => void;
  handleImageChange: (
    event: React.ChangeEvent<HTMLInputElement>
  ) => Promise<void>;
  isMessageSending: boolean;
  isImageUploading: boolean;
  selectedImage: File | null;
  onRemoveImage: () => void;
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleRemoveImageWithReset = () => {
    // Reset the file input value
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
    onRemoveImage();
  };
  return (
    <Box
      sx={{
        width: "100%",
        maxWidth: 800,
        margin: "20px 0",
      }}
    >
      {(selectedImage || isImageUploading) && (
        <Box
          sx={{
            mb: 2,
            p: 2,
            border: "1px solid #ccc",
            borderRadius: "8px",
            backgroundColor: "#f9f9f9",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            opacity: isMessageSending ? 0.6 : 1,
            pointerEvents: isMessageSending ? "none" : "auto",
          }}
        >
          <Box sx={{ display: "flex", alignItems: "center" }}>
            <Typography variant="subtitle2" sx={{ mr: 2 }}>
              {isImageUploading ? "Processing Image..." : "Selected Image:"}
            </Typography>
            {isImageUploading ? (
              <Box
                sx={{
                  width: "100px",
                  height: "100px",
                  borderRadius: "4px",
                  backgroundColor: "#e0e0e0",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <CircularProgress size={40} />
              </Box>
            ) : (
              selectedImage && (
                <img
                  src={URL.createObjectURL(selectedImage)}
                  alt="Selected"
                  style={{
                    maxWidth: "100px",
                    maxHeight: "100px",
                    borderRadius: "4px",
                    objectFit: "cover",
                  }}
                />
              )
            )}
          </Box>
          {!isImageUploading && (
            <IconButton
              onClick={handleRemoveImageWithReset}
              size="small"
              sx={{ color: "#666" }}
              disabled={isMessageSending}
            >
              <Close />
            </IconButton>
          )}
        </Box>
      )}

      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <input
          ref={fileInputRef}
          accept="image/*"
          style={{ display: "none" }}
          id="icon-button-file"
          type="file"
          onChange={handleImageChange}
          disabled={isMessageSending || isImageUploading}
        />
        <label htmlFor="icon-button-file">
          <IconButton
            disabled={isMessageSending || isImageUploading}
            color="primary"
            aria-label="upload picture"
            component="span"
          >
            {isImageUploading ? (
              <CircularProgress size={24} />
            ) : (
              <PhotoCamera />
            )}
          </IconButton>
        </label>
        <TextField
          disabled={isMessageSending}
          fullWidth
          label="輸入訊息"
          variant="outlined"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === "Enter") sendMessage();
          }}
          sx={{ mr: 2 }}
        />
        <Button
          loading={isMessageSending}
          variant="contained"
          color="primary"
          onClick={sendMessage}
          disabled={isMessageSending}
        >
          發送
        </Button>
      </Box>
    </Box>
  );
};
