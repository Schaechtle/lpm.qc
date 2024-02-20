---
theme: dashboard
title: 1-D Marginals
toc: true
---

# Synthetic data QC - PoC 🧐

Below, we analyze one-dimensional goodness of fit for synthetic data. We look at each column individually. This section does *not* consider multivariate interactions in the data.

We analyze the fit in two ways.
1. **We assess goodness of fit.** We use compute total variation distance between training data and synthetic data and training data and real held-out data. For each method for creating synthetic data, we show the best and worst-fit columns.
2. **We use statistical tests to assess whether synthetic and real data are different.** We use a two-sample test to assess, for each column, whether the synthetic data differs from the real data.


## Goodness of fit

### Legend
<style>
  /* Apply styles to all list items within the body */
  body li {
    color: black; /* Example color: blue */
  }

  /* Alternatively, if you want different colors for each item,
     you can assign classes to them and style those classes. */
  .red { color: red; }
  .black { color: black; }
  .syn { color: #f28e2b; }
</style>

<ul>
  <li class="black">Observed real data</li>
  <li class="syn">IQL synthetic data </li>
  <li class="red">Baseline synthetic data (maximum entropy distribution)</li>
</ul>

<!-- Load and transform the data -->

```js
const distance_held_out = FileAttachment("data/distance-metrics/corr.csv").csv({typed: true});
```


```js
function discrete1dBar(column, data) {
  return {
    "data": {
      "url": data
    },
    concat: [
    {"concat":
     [{"mark":
       {"type":"bar",
        "color":"lightgrey",
        "tooltip":{"content":"data"}},
       "transform":
       [{"window":[{"op":"row_number", "as":"row_number_subplot"}],
         "groupby":["collection"]},
        {"filter":
         {"and":
          [{"field":"collection", "equal":"observed"},
           {"field":"row_number_subplot", "lte":1000},
           {"field":"row_number_subplot",
            "lte":{"expr":400}}]}}],
       "encoding":
       {"y":
        {"bin":false,
         "field":column,
         "type":"nominal",
         "axis":
         {"titleAnchor":"start",
          "titleAlign":"right",
          "titlePadding":1}},
        "x":
        {"aggregate":"count",
         "type":"quantitative",
         "scale":{"domain":[0, 222.20000000000002]},
         "axis":{"orient":"top"}},
        "color":{"value":"#000000"}}},
    {"mark":
       {"type":"bar",
        "color":"lightgrey",
        "tooltip":{"content":"data"}},
       "transform":
       [{"window":[{"op":"row_number", "as":"row_number_subplot"}],
         "groupby":["collection"]},
        {"filter":
         {"and":
          [{"field":"collection", "equal":"iql"},
           {"field":"row_number_subplot", "lte":1000},
           {"field":"row_number_subplot",
            "lte":{"expr":400}}]}}],
       "encoding":
       {"y":
        {"bin":false,
         "field": column,
         "type":"nominal",
         "axis":
         {"titleAnchor":"start",
          "titleAlign":"right",
          "titlePadding":1}},
        "x":
        {"aggregate":"count",
         "type":"quantitative",
         "scale":{"domain":[0, 222.20000000000002]},
         "axis":{"orient":"top"}},
        "color":{"value":"#f28e2b"}}},
      {"mark":
       {"type":"bar",
        "color":"lightgrey",
        "tooltip":{"content":"data"}},
       "transform":
       [{"window":[{"op":"row_number", "as":"row_number_subplot"}],
         "groupby":["collection"]},
        {"filter":
         {"and":
          [{"field":"collection", "equal":"baseline"},
           {"field":"row_number_subplot", "lte":1000},
           {"field":"row_number_subplot",
            "lte":{"expr":400}}]}}],
       "encoding":
       {"y":
        {"bin":false,
         "field": column,
         "type":"nominal",
         "axis":
         {"titleAnchor":"start",
          "titleAlign":"right",
          "titlePadding":1}},
        "x":
        {"aggregate":"count",
         "type":"quantitative",
         "scale":{"domain":[0, 222.20000000000002]},
         "axis":{"orient":"top"}},
        "color":{"value":"red"}}}]}]}
}
```

```js
const data = await FileAttachment("data/comp.csv").url();
```

```js
const best = await FileAttachment("data/best.csv").csv({typed: true});
```

```js
const worst = await FileAttachment("data/worst.csv").csv({typed: true});
```

### Best fit - LPM

Best fitting column under the LPM:
```js
vl.render({spec:discrete1dBar(best[0].iql, data)})
```
Second best fitting column under the LPM:
```js
vl.render({spec:discrete1dBar(best[1].iql, data)})
```

### Worst fit - LPM

Worst fitting column under the LPM:
```js
vl.render({spec:discrete1dBar(worst[2].iql, data)})
```
Second worst fitting column under the LPM:
```js
vl.render({spec:discrete1dBar(worst[1].iql, data)})
```

### Best fit - Max entropy (baseline)

Best fitting column under the baseline:
```js
vl.render({spec:discrete1dBar(best[0].me, data)})
```
Second best fitting column under the baseline:
```js
vl.render({spec:discrete1dBar(best[1].me, data)})
```

### Worst  fit - Max entropy (baseline)

Worst fitting column under the baseline:
```js
vl.render({spec:discrete1dBar(worst[2].me, data)})
```
Second worst fitting column under the baseline:
```js
vl.render({spec:discrete1dBar(worst[1].me, data)})
```

### Overview over Correlation between distance metrics

```js
import * as vega from "npm:vega";
import * as vegaLite from "npm:vega-lite";
import * as vegaLiteApi from "npm:vega-lite-api";

const vl = vegaLiteApi.register(vega, vegaLite);
```

```js
vl.render({
  spec: {
    "width": 400,
    "height": 400,
    "data": {
      "url": await FileAttachment("data/distance-metrics/corr.csv").url()
    },
    "layer": [
    {
        "mark": "point",
        "encoding": {
              "x": {
                "type": "quantitative",
                "field": "iql",
                "scale": {"domain": [0, 0.5]},
                "axis": {"title":"Distance of IQL synthetic data to training data"}
              },
              "y": {
                "type": "quantitative",
                "field": "held-out",
                "scale": {"domain": [0, 0.5]},
                "axis": {
                    "title":"Distance of held-out data to training data",
                    "titleAngle": 0,
                    "titleAlign": "right"
                    }
                }
            }
    },
    {
          "data": {
            "values": [
              {"x": 0.0, "y": 0.0},
              {"x": 0.5, "y":  0.5}
            ]
          },
          "mark": {
                "type": "line",
                "strokeDash": [5, 5] // This creates the dashed pattern, adjust numbers for different patterns
              },
              "encoding": {
                "x": {
                    "field": "x",
                    "type": "quantitative",
                    "axis": {"title":"Distance of IQL synthetic data to training data"}
                },
                "y": {
                    "field": "y",
                    "type": "quantitative",
                    "axis": {
                        "title":"Distance of held-out data to training data",
                        "titleAngle": 0,
                        "titleAlign": "right"
                        }
                    }
              }
    }
    ]
  }
})
```

## Statistical testing

### IQL
```js
const statsIQL = FileAttachment("data/statsIQL.csv").csv({typed: true});
```

<div class="card" style="padding: 0;">
${Inputs.table(statsIQL, {rows: 16})}
</div>


### Baseline

```js
const statsME = FileAttachment("data/statsME.csv").csv({typed: true});
```

<div class="card" style="padding: 0;">
${Inputs.table(statsME, {rows: 16})}
</div>
