import { Route, Routes } from "react-router-dom";
import EmailCheckPage from "./features/auth/pages/EmailCheckPage";
import RegisterPage from "./features/auth/pages/RegisterPage";
import BookingPage from "./features/booking/pages/BookingPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<EmailCheckPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/booking" element={<BookingPage />} />
    </Routes>
  );
}

export default App;