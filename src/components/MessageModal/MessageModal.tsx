"use client";

import "./messageModal.css";
import { useUIStore } from "@/context/useUIStore";
import React from "react";
import { Button } from "../Button";
import Image from "next/image";

export function MessageModal() {
  const { isMessageModalOpen, messageModalContent, closeMessageModal } =
    useUIStore();

  return (
    <>
      {isMessageModalOpen ? (
        <div className="modal-backdrop" onClick={closeMessageModal}>
          {!messageModalContent.loading ? (
            <div className="message-modal-container">
              <div className="min-h-[150px] border border-black dark:border-white">
                <h1 className="p-2 border-b border-black dark:border-white">
                  {messageModalContent.title}
                </h1>
                <div className="grow p-2">
                  <p>{messageModalContent.message}</p>
                </div>
              </div>
              <Button
                className="mt-[-1px]"
                variant="outlined"
                onClick={closeMessageModal}
              >
                CLOSE
              </Button>
            </div>
          ) : (
            <div className="loading-modal-container">
              <Image
                src="/loading.svg"
                alt="loading-icon"
                width={0}
                height={0}
                className="icon h-full w-auto"
              />
            </div>
          )}
        </div>
      ) : null}
    </>
  );
}
