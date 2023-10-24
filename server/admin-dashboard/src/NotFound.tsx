import React from "react";

import NotFoundPage from "./components/NotFoundPage";
import useNavigator from "./hooks/useNavigator";

export const NotFound: React.FC = () => {
  const navigate = useNavigator();

  return <NotFoundPage onBack={() => navigate("/")} />;
};
export default NotFound;
