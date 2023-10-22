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
  setMessageModalContent: (content: MessageModalContent) => void;
  setLoadingModalContent: <T>(
    promise: Promise<T>,
    resolver: (input: T) => MessageModalContent
  ) => void;
}

export const useUIStore = create<UIStoreType>()((set) => ({
  currentCategoryIndex: 0,
  setCurrentCategoryIndex: (i) => set(() => ({ currentCategoryIndex: i })),

  isSidebarOpen: false,
  toggleSidebar: () =>
    set(({ isSidebarOpen }) => ({ isSidebarOpen: !isSidebarOpen })),

  isMessageModalOpen: false,
  messageModalContent: { title: "", message: "" },
  setMessageModalContent: (content) =>
    set(() => ({ messageModalContent: { ...content, loading: false } })),
  setLoadingModalContent: async <T>(
    promise: Promise<T>,
    resolver: (input: T) => MessageModalContent
  ) => {
    set(({ messageModalContent }) => ({
      messageModalContent: { ...messageModalContent, loading: true },
    }));
    const content = await promise.then(resolver);
    set(() => ({ messageModalContent: { ...content, loading: false } }));
  },
}));
