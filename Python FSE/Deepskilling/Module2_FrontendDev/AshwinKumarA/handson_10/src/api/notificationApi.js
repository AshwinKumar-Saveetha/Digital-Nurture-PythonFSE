import apiClient from "./apiClient";

export async function getLatestNotifications(limit = 5) {
  const notifications = await apiClient.get("/posts", {
    params: {
      _limit: limit,
    },
  });

  return notifications.map((notification) => ({
    id: notification.id,
    title: notification.title,
    message: notification.body,
  }));
}