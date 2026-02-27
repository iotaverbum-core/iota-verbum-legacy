import { useMutation, useQuery } from "@tanstack/react-query";
import { Pressable, ScrollView, StyleSheet, Text, View } from "react-native";

import { getDeviceId, getShapeForCurrentDevice, postMoment } from "../src/lib/api";

export default function DebugScreen() {
  const shapeQuery = useQuery({
    queryKey: ["shape", "debug"],
    queryFn: getShapeForCurrentDevice,
    retry: false,
  });

  const sampleMutation = useMutation({
    mutationFn: async () => {
      const deviceId = await getDeviceId();
      const response = await postMoment(
        "I feel pulled in several directions, but I choose to release the outcome.",
        false,
        true
      );
      return { deviceId, response };
    },
    onSuccess: () => {
      shapeQuery.refetch();
    },
  });

  return (
    <View style={styles.screen}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>Presence Debug</Text>
        <Text style={styles.label}>shape response</Text>
        <Text style={styles.json}>
          {JSON.stringify(shapeQuery.data ?? { error: shapeQuery.error instanceof Error ? shapeQuery.error.message : null }, null, 2)}
        </Text>
        <Pressable
          style={[styles.button, sampleMutation.isPending && styles.buttonDisabled]}
          disabled={sampleMutation.isPending}
          onPress={() => sampleMutation.mutate()}
        >
          <Text style={styles.buttonText}>{sampleMutation.isPending ? "Posting..." : "POST sample moment"}</Text>
        </Pressable>
        {sampleMutation.error ? (
          <Text style={styles.error}>
            {sampleMutation.error instanceof Error ? sampleMutation.error.message : "Failed posting sample entry"}
          </Text>
        ) : null}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: "#fff",
  },
  content: {
    paddingTop: 52,
    paddingHorizontal: 16,
    paddingBottom: 32,
    gap: 12,
  },
  title: {
    color: "#111",
    fontSize: 22,
  },
  label: {
    color: "#444",
    fontSize: 12,
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  json: {
    color: "#111",
    fontSize: 13,
    fontFamily: "monospace",
    borderWidth: 1,
    borderColor: "#111",
    padding: 12,
  },
  button: {
    borderWidth: 1,
    borderColor: "#111",
    paddingVertical: 12,
    alignItems: "center",
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: "#111",
  },
  error: {
    color: "#a40000",
    fontSize: 12,
  },
});
