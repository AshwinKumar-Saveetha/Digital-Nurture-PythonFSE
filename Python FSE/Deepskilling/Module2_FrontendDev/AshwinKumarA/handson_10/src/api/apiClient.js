import axios from "axios";

const apiClient = axios.create({
  baseURL: "https://jsonplaceholder.typicode.com",
  timeout: 10000,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const updatedConfig = { ...config };

    updatedConfig.headers = {
      ...updatedConfig.headers,
      Authorization: "Bearer mock-student-portal-token",
    };

    console.log(`API call started: ${updatedConfig.url}`);

    return updatedConfig;
  },
  (requestError) => {
    return Promise.reject(requestError);
  },
);

apiClient.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (axiosError) => {
    const statusCode = axiosError.response?.status ?? 0;

    const message =
      axiosError.response?.data?.message ||
      axiosError.message ||
      "An unexpected API error occurred.";

    const standardisedError = new Error(message);

    standardisedError.statusCode = statusCode;

    return Promise.reject(standardisedError);
  },
);

export default apiClient;