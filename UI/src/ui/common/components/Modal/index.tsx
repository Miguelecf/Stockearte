import React from "react";
import * as Styles from "./styles";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: () => void;
  title: string;
  children: React.ReactNode;
}

const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  onSave,
  title,
  children,
}) => {
  if (!isOpen) return null;

  return (
    <Styles.ModalBackdrop>
      <Styles.ModalContent>
        <Styles.CloseButton onClick={onClose}>&times;</Styles.CloseButton>
        <Styles.ModalHeader>{title}</Styles.ModalHeader>
        <Styles.ModalBody>{children}</Styles.ModalBody>
        <Styles.ModalFooter>
          <Styles.CancelButton onClick={onClose}>Cancel</Styles.CancelButton>
          <Styles.SaveButton onClick={onSave}>Save</Styles.SaveButton>
        </Styles.ModalFooter>
      </Styles.ModalContent>
    </Styles.ModalBackdrop>
  );
};

export default Modal;
