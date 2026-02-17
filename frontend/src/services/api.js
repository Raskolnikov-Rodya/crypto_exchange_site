import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common.Authorization;
  }
};

export const authApi = {
  register: (payload) => api.post("/auth/register", payload),
  login: (email, password) => {
    const body = new URLSearchParams();
    body.append("username", email);
    body.append("password", password);
    return api.post("/auth/login", body, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
  },
  me: () => api.get("/auth/me"),
};

export const walletApi = {
  balances: () => api.get("/wallet/balances"),
  deposit: (payload) => api.post("/wallet/deposit", payload),
  requestWithdraw: (payload) => api.post("/wallet/withdraw/request", payload),
  myWithdrawals: () => api.get("/wallet/withdraw/requests"),
};

export const adminApi = {
  credit: (payload) => api.post("/admin/credit", payload),
  withdrawals: () => api.get("/admin/withdrawals"),
  approveWithdrawal: (id, payload = {}) => api.post(`/admin/withdrawals/${id}/approve`, payload),
  rejectWithdrawal: (id, payload = {}) => api.post(`/admin/withdrawals/${id}/reject`, payload),
  completeWithdrawal: (id, payload = {}) => api.post(`/admin/withdrawals/${id}/complete`, payload),
};
