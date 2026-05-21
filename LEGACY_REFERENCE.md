# Legacy Reference

The legacy reference project is:

```text
E:\physics\CharacteristicImpedanceLegacy
```

It preserves the original BigCalc2 C# / WinForms exploration. The important
early workflow was:

- load pre-2019 CODATA text,
- parse significant digits,
- convert those digits into binary,
- run circular XOR evolution,
- compare forward/reverse/inverse/inverse-reverse outputs,
- scan generated runs for other constant bit patterns.

Use the legacy project to recover original formulas, constants, exploratory
data, GUI behavior, and historical experiments.

Do not mechanically port the GUI. Extract concepts and rebuild them as testable
Python modules.
