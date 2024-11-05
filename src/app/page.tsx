'use client'

import Image from "next/image";
import { usePathname } from "next/navigation"; // Импортируем usePathname для доступа к текущему маршруту
import WelcomePage from "./pages/WelcomePage";
import Login from "./pages/Login";
import PasswordResetForm from "./molecules/PasswordResetForm/PasswordResetForm";
import VacancyRegisterTemplate from "./templates/VacancyRegisterTemplate/VacancyRegisterTemplate";
import RegisterTemplate from "./templates/RegisterTemplate/RegisterTemplate";

export default function Home() {
  const pathname = usePathname();
  const renderComponent = () => {
    switch (pathname) {
      case "/login":
        return <Login />;
      case "/register":
        return <RegisterTemplate />;
      case "/password-reset":
        return <PasswordResetForm />;
      case "/vacancy-registeration":
        return <VacancyRegisterTemplate />;
      default:
        return <WelcomePage />;
    }
  };

  return (
    <div>
      {renderComponent()} 
    </div>
  );
}
