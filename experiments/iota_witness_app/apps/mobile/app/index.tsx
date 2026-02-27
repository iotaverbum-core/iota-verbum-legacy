import { useQuery } from "@tanstack/react-query";
import { router } from "expo-router";
import { useEffect } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

import { getShapeForCurrentDevice } from "../src/lib/api";

export default function HomeScreen() {
  const shapeQuery = useQuery({
    queryKey: ["shape"],
    queryFn: getShapeForCurrentDevice,
    retry: 1,
    refetchInterval: 15000,
  });

  useEffect(() => {
    if (shapeQuery.error) {
      console.warn("[presence] shape_fetch_failed", shapeQuery.error);
    }
  }, [shapeQuery.error]);

  const symbol = shapeQuery.data?.symbol ?? "\u25A1";

  return (
    <View style={styles.screen}>
      <Pressable
        onLongPress={() => router.push("/debug")}
        delayLongPress={500}
        accessibilityLabel="Presence symbol"
      >
        <Text style={styles.symbol}>{symbol}</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: "#fff",
    justifyContent: "center",
    alignItems: "center",
  },
  symbol: {
    fontSize: 148,
    lineHeight: 160,
    color: "#111",
    fontWeight: "400",
  },
});
