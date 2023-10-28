import { create } from "zustand";

type MessageModalContent = {
  title: string;
  message: string;
  loading?: boolean;
};

interface UIStoreType {
  currentCategoryIndex: number;
  setCurrentCategoryIndex: (i: number) => void;

  isSidebarOpen: boolean;
  toggleSidebar: () => void;

  isMessageModalOpen: boolean;
  messageModalContent: MessageModalContent;
  closeMessageModal: () => void;
  setMessageModalContent: (content: MessageModalContent) => void;
  setLoadingModalContent: <T>(
    promise: Promise<T>,
    resolver: (input: T) => MessageModalContent | null
  ) => Promise<T>;
}

export const useUIStore = create<UIStoreType>()((set) => ({
  currentCategoryIndex: 0,
  setCurrentCategoryIndex: (i) => set(() => ({ currentCategoryIndex: i })),

  isSidebarOpen: false,
  toggleSidebar: () =>
    set(({ isSidebarOpen }) => ({ isSidebarOpen: !isSidebarOpen })),

  isMessageModalOpen: false,
  messageModalContent: { title: "", message: "" },
  // should not close message modal when the loading attribute is true
  closeMessageModal: () =>
    set(({ isMessageModalOpen, messageModalContent }) => ({
      isMessageModalOpen: messageModalContent.loading
        ? isMessageModalOpen
        : false,
    })),
  setMessageModalContent: (content) =>
    set(() => ({
      isMessageModalOpen: true,
      messageModalContent: { ...content, loading: false },
    })),
  setLoadingModalContent: async <T>(
    promise: Promise<T>,
    resolver: (input: T) => MessageModalContent | null
  ) => {
    set(({ messageModalContent }) => ({
      isMessageModalOpen: true,
      messageModalContent: { ...messageModalContent, loading: true },
    }));
    let response;
    const content = await promise
      .then((res) => {
        response = res;
        return resolver(res);
      })
      .catch((err) => ({ title: "Unexpected Error", message: err }));
    if (content !== null) {
      set(() => ({
        messageModalContent: { ...content, loading: false },
      }));
    } else {
      set(() => ({
        isMessageModalOpen: false,
      }));
    }
    return response as T;
  },
}));
