import React from 'react';
import PeriodComponent from './PeriodComponent';
import { Bar } from 'react-chartjs-2';
import SelectButtonComponent from './SelectButtonComponent'

function AverageBuySellComponent({ onClick, data, name }) {
  return (

    <div className="chart" align="left" id="dataAverageBuySellPrices" type="text/css" href="chart.css">
      <form id="formParams"  >
        <table id="tableParams" className="tableParams" align="left" cellSpacing="0" >
          <tbody>
            <PeriodComponent name={name} />
            <SelectButtonComponent onClick={onClick} />
          </tbody>
        </table>
      </form>
      <h2>Average Buy&Sell prices</h2>
      <Bar data={data}>

      </Bar>

    </div>
  );
}

export default AverageBuySellComponent;