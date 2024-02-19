---
theme: dashboard
title: Tables
toc: false
---

# Data tables

Below, we show real data and synthetic data used in the current QC benchmarking efforts.

```js
const training = FileAttachment("data/training.csv").csv({typed: true});
const held_out = FileAttachment("data/held.csv").csv({typed: true});
const lpm_data = FileAttachment("data/lpm.csv").csv({typed: true});
const max_entropy_data = FileAttachment("data/max_entropy.csv").csv({typed: true});
```

<!-- Load and transform the data
 -->

<style>
  body {
    font-family: Arial, sans-serif;
  }

  /* Style the tab container */
  .tab {
    overflow: hidden;
    background-color: #fff;
    border: 1px solid #ccc;
    border-bottom: none;
    padding: 0;
    margin: 0;
  }

  /* Style the buttons inside the tab */
  .tab button {
    background-color: #f2f2f2;
    float: left;
    border: none;
    outline: none;
    cursor: pointer;
    padding: 10px 15px;
    transition: 0.3s;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 2px;
  }

  /* Change background color of buttons on hover */
  .tab button:hover {
    background-color: #e7e7e7;
  }

  /* Style the active tab */
  .tab button.active {
    background-color: #fff;
    border-bottom: 1px solid white;
  }

  /* Style the tab content */
  .tabcontent {
    display: none;
    padding: 20px;
    border: 1px solid #ccc;
    border-top: none;
    animation: fadeIn 0.5s;
  }

  @keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
  }
</style>


<!-- This should probably go into a JS tag -->
<script>
function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}
</script>

## Real data

```html
<div class="tab">
  <button class="tablinks" onclick="openTab(event, 'Training data')">Training data</button>
  <button class="tablinks" onclick="openTab(event, 'Held-out data')">Held-out data</button>
</div>

<div id="Training data" class="tabcontent">
<div class="card" style="padding: 0;">
  ${Inputs.table(training, {rows: 16})}
</div>
</div>

<div id='Held-out data' class="tabcontent">
<div class="card" style="padding: 0;">
  ${Inputs.table(held_out, {rows: 16})}
</div>
</div>
```

## Synthetic data

```html
<div class="tab">
  <button class="tablinks" onclick="openTab(event, 'LPM')"> LPM </button>
  <button class="tablinks" onclick="openTab(event, 'Max entropy (baseline)')">Max entropy (baseline)</button>
</div>

<div id="LPM" class="tabcontent">
<div class="card" style="padding: 0;">
  ${Inputs.table(lpm_data, {rows: 16})}
</div>
</div>

<div id='Max entropy (baseline)' class="tabcontent">
<div class="card" style="padding: 0;">
  ${Inputs.table(max_entropy_data, {rows: 16})}
</div>
</div>
```

