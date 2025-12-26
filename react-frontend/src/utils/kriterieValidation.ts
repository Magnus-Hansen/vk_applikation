// Validation function matching backend Pydantic models
export const validateKriterie = (data: any): { valid: boolean; errors: string[] } => {
  const errors: string[] = [];

  // Check if it's an array or single object
  const items = Array.isArray(data) ? data : [data];

  items.forEach((item, index) => {
    const stationId = item.station_id || "unknown";
    const prefix = Array.isArray(data) ? `Item ${index + 1} (${stationId}): ` : "";

    // Required field: station_id (must be exactly 8 characters)
    if (!item.station_id) {
      errors.push(`${prefix}Missing required field "station_id"`);
    } else if (typeof item.station_id !== "string") {
      errors.push(`${prefix}"station_id" must be a string`);
    } else if (item.station_id.length !== 8) {
      errors.push(`${prefix}"station_id" must be exactly 8 characters (got ${item.station_id.length})`);
    }

    // Optional: id field (if present, must be a number)
    if (item.id !== undefined && item.id !== null && typeof item.id !== "number") {
      errors.push(`${prefix}"id" must be a number`);
    }

    // Check for unknown top-level fields (catch typos)
    const validTopLevelFields = ["id", "station_id", "dkhype", "vandstand"];
    Object.keys(item).forEach((key) => {
      if (!validTopLevelFields.includes(key)) {
        errors.push(`${prefix}Unknown field "${key}" (possible typo? Expected: ${validTopLevelFields.join(", ")})`);
      }
    });

    // Validate dkhype object if present
    if (item.dkhype !== undefined && item.dkhype !== null) {
      if (typeof item.dkhype !== "object") {
        errors.push(`${prefix}"dkhype" must be an object`);
      } else {
        const validDkhypeFields = ["1.1", "5", "20", "50"];
        Object.keys(item.dkhype).forEach((key) => {
          if (!validDkhypeFields.includes(key)) {
            errors.push(`${prefix}"dkhype" has invalid field "${key}"`);
          }
          const value = item.dkhype[key];
          if (value !== null && value !== "" && typeof value !== "number") {
            errors.push(`${prefix}"dkhype.${key}" must be a number, null, or empty string`);
          } else if (typeof value === "number" && value < 0) {
            errors.push(`${prefix}"dkhype.${key}" cannot be negative (got ${value})`);
          }
        });

        // Check ascending order: 1.1 < 5 < 20 < 50
        const d = item.dkhype;
        const vals = {
          "1.1": d["1.1"],
          "5": d["5"],
          "20": d["20"],
          "50": d["50"]
        };
        
        // Filter out null/empty values for comparison
        const numVals: { [key: string]: number } = {};
        (Object.keys(vals) as Array<keyof typeof vals>).forEach(k => {
          if (vals[k] !== null && vals[k] !== "") {
            numVals[k] = vals[k];
          }
        });

        if (numVals["1.1"] !== undefined && numVals["5"] !== undefined && numVals["1.1"] >= numVals["5"]) {
          errors.push(`${prefix}"dkhype.1.1" (${numVals["1.1"]}) must be less than "dkhype.5" (${numVals["5"]})`);
        }
        if (numVals["5"] !== undefined && numVals["20"] !== undefined && numVals["5"] >= numVals["20"]) {
          errors.push(`${prefix}"dkhype.5" (${numVals["5"]}) must be less than "dkhype.20" (${numVals["20"]})`);
        }
        if (numVals["20"] !== undefined && numVals["50"] !== undefined && numVals["20"] >= numVals["50"]) {
          errors.push(`${prefix}"dkhype.20" (${numVals["20"]}) must be less than "dkhype.50" (${numVals["50"]})`);
        }
      }
    }

    // Validate vandstand object if present
    if (item.vandstand !== undefined && item.vandstand !== null) {
      if (typeof item.vandstand !== "object") {
        errors.push(`${prefix}"vandstand" must be an object`);
      } else {
        const validVandstandFields = ["varsel", "1.1", "2", "5", "10"];
        Object.keys(item.vandstand).forEach((key) => {
          if (!validVandstandFields.includes(key)) {
            errors.push(`${prefix}"vandstand" has invalid field "${key}"`);
          }
          const value = item.vandstand[key];
          if (value !== null && value !== "" && typeof value !== "number") {
            errors.push(`${prefix}"vandstand.${key}" must be a number, null, or empty string`);
          } else if (typeof value === "number" && value < 0) {
            errors.push(`${prefix}"vandstand.${key}" cannot be negative (got ${value})`);
          }
        });

        // Check ascending order: 1.1 < 2 < 5 < 10 (varsel not included in ordering)
        const v = item.vandstand;
        const vals = {
          "1.1": v["1.1"],
          "2": v["2"],
          "5": v["5"],
          "10": v["10"]
        };
        
        // Filter out null/empty values for comparison
        const numVals: { [key: string]: number } = {};
        (Object.keys(vals) as Array<keyof typeof vals>).forEach(k => {
          if (vals[k] !== null && vals[k] !== "") {
            numVals[k] = vals[k];
          }
        });

        if (numVals["1.1"] !== undefined && numVals["2"] !== undefined && numVals["1.1"] >= numVals["2"]) {
          errors.push(`${prefix}"vandstand.1.1" (${numVals["1.1"]}) must be less than "vandstand.2" (${numVals["2"]})`);
        }
        if (numVals["2"] !== undefined && numVals["5"] !== undefined && numVals["2"] >= numVals["5"]) {
          errors.push(`${prefix}"vandstand.2" (${numVals["2"]}) must be less than "vandstand.5" (${numVals["5"]})`);
        }
        if (numVals["5"] !== undefined && numVals["10"] !== undefined && numVals["5"] >= numVals["10"]) {
          errors.push(`${prefix}"vandstand.5" (${numVals["5"]}) must be less than "vandstand.10" (${numVals["10"]})`);
        }
      }
    }
  });

  return {
    valid: errors.length === 0,
    errors
  };
};
