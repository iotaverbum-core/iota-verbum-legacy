import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { useState } from "react";

export default function RootLayout() {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <StatusBar style="dark" />
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="index" />
        <Stack.Screen name="debug" />
        <Stack.Screen name="season" />
        <Stack.Screen name="moment" />
        <Stack.Screen name="trace" />
        <Stack.Screen name="response" />
        <Stack.Screen name="settings" />
      </Stack>
    </QueryClientProvider>
  );
}
