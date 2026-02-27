import { PropsWithChildren } from "react";
import { StyleSheet, Text, View } from "react-native";

export function Screen({ children }: PropsWithChildren) {
  return <View style={styles.screen}>{children}</View>;
}

export function SymbolsHeader() {
  return <Text style={styles.header}>□ ◇ → Δ</Text>;
}

export const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: "#ffffff",
    paddingHorizontal: 20,
    paddingTop: 56,
    paddingBottom: 28
  },
  header: {
    color: "#111111",
    letterSpacing: 3,
    fontSize: 22,
    marginBottom: 20,
    fontWeight: "500"
  }
});
