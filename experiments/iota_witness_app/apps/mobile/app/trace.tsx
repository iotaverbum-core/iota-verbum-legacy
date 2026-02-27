import { useQuery } from "@tanstack/react-query";
import { Pressable, ScrollView, StyleSheet, Text } from "react-native";

import { deleteMyData, getTrace } from "../src/lib/api";
import { Screen, SymbolsHeader } from "../src/ui/primitives";

export default function TraceScreen() {
  const trace = useQuery({ queryKey: ["trace"], queryFn: getTrace, retry: false });

  return (
    <Screen>
      <SymbolsHeader />
      <ScrollView>
        <Text style={styles.title}>Trace</Text>
        {trace.isLoading ? <Text style={styles.line}>Loading...</Text> : null}
        {trace.error ? <Text style={styles.line}>No trace yet.</Text> : null}
        {trace.data ? (
          <>
            <Text style={styles.line}>Dominant distortion: {trace.data.dominant_distortion}</Text>
            <Text style={styles.line}>Velocity trend: {trace.data.velocity_trend.toFixed(3)}</Text>
            <Text style={styles.line}>Hinge consistency: {trace.data.hinge_consistency.toFixed(3)}</Text>
            <Text style={styles.line}>Entrustment stability: {trace.data.entrustment_stability.toFixed(3)}</Text>
            <Text style={styles.line}>Samples: {trace.data.sample_count}</Text>
          </>
        ) : null}
        <Pressable
          style={styles.button}
          onPress={async () => {
            await deleteMyData();
            trace.refetch();
          }}
        >
          <Text style={styles.buttonText}>Delete My Data</Text>
        </Pressable>
      </ScrollView>
    </Screen>
  );
}

const styles = StyleSheet.create({
  title: {
    color: "#111",
    fontSize: 22,
    marginBottom: 12
  },
  line: {
    color: "#111",
    fontSize: 16,
    marginBottom: 8
  },
  button: {
    marginTop: 20,
    borderWidth: 1,
    borderColor: "#111",
    paddingVertical: 12,
    alignItems: "center"
  },
  buttonText: {
    color: "#111"
  }
});
