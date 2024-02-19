---
theme: dashboard
title: 1-D Marginals
toc: false
---

# Synthetic data QC - PoC 🚀

<!-- Load and transform the data -->

```js
const distance_held_out = FileAttachment("data/distance-metrics/corr.csv").csv({typed: true});
```

<!-- Load and transform the data
```js
display(distance_held_out);
```
 -->

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

```js
vl.render({
  spec: {
    "data": {
      "url": await FileAttachment("data/comp.csv").url()
    },
    concat: [{"concat":
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
           {"field":"row_number_subplot", "lte":450},
           {"field":"row_number_subplot",
            "lte":{"expr":400}}]}}],
       "encoding":
       {"y":
        {"bin":false,
         "field":"Type_of_Orbit",
         "type":"nominal",
         "axis":
         {"titleAnchor":"start",
          "titleAlign":"right",
          "titlePadding":1}},
        "x":
        {"aggregate":"count",
         "type":"quantitative",
         "scale":{"domain":[0, 325.05]},
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
          [{"field":"collection", "equal":"synthetic"},
           {"field":"row_number_subplot", "lte":450},
           {"field":"row_number_subplot",
            "lte":{"expr":400}}]}}],
       "encoding":
       {"y":
        {"bin":false,
         "field":"Type_of_Orbit",
         "type":"nominal",
         "axis":
         {"titleAnchor":"start",
          "titleAlign":"right",
          "titlePadding":1}},
        "x":
        {"aggregate":"count",
         "type":"quantitative",
         "scale":{"domain":[0, 325.05]},
         "axis":{"orient":"top"}},
        "color":{"value":"#f28e2b"}}}]},
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
       "params":
       [{"name":"brush-all",
         "select":
         {"type":"point",
          "nearest":true,
          "toggle":"true",
          "on":"click[!event.shiftKey]",
          "fields":["Launch_Site", "collection"],
          "clear":"dblclick[!event.shiftKey]"}}],
       "encoding":
       {"y":
        {"bin":false,
         "field":"Launch_Site",
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
          [{"field":"collection", "equal":"synthetic"},
           {"field":"row_number_subplot", "lte":1000},
           {"field":"row_number_subplot",
            "lte":{"expr":400}}]}}],
       "params":
       [{"name":"brush-all",
         "select":
         {"type":"point",
          "nearest":true,
          "toggle":"true",
          "on":"click[!event.shiftKey]",
          "fields":["Launch_Site", "collection"],
          "clear":"dblclick[!event.shiftKey]"}}],
       "encoding":
       {"y":
        {"bin":false,
         "field":"Launch_Site",
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
        "color":{"value":"#f28e2b"}}}]}]}})
```

