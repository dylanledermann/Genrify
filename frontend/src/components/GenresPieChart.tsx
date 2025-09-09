'use client'

import {
    Card,
    CardBody
} from "@material-tailwind/react";
import dynamic from "next/dynamic";
import { Suspense, useState } from "react";

type Props = {
    genres: any,
    callback: (genre: string | null) => void
}

const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

const GenresPieChart = ({genres, callback}: Props) => {
    const [prev, setPrev] = useState<string | null>(null)
    const chartConfig = {
        type: "pie",
        series: genres.map((arr:[string, number])=>(
            arr[1]
        )),
        options: {
            theme: {
                mode: 'dark',
            },
            chart: {
                events: {
                    dataPointSelection: function(event: any, chartContext: any, config: { w: { config: { labels: { [x: string]: any; }; }; }; dataPointIndex: string | number; }) {
                      // Get the label name
                      var clickedValue = config.w.config.labels[config.dataPointIndex];
                      if(prev === clickedValue){
                        callback(null);
                        setPrev(null)
                      }
                      else{
                        callback(clickedValue);
                        setPrev(clickedValue);
                      }
                    }
                },
                background: '#212121',
                toolbar: {
                show: false,
                },
            },
            labels: genres.map((arr:[string, number])=>(
                arr[0]
            )),
            title: {
                show: "",
            },
            dataLabels: {
                enabled: false,
            },
            // colors: ["#020617", "#ff8f00", "#00897b", "#1e88e5", "#d81b60"],
            legend: {
                show: false,
            },
        },
    };

    return (
        <>  
        <Suspense fallback={
            <div className="flex justify-center items-center h-[280px] w-full">
                <div className="w-16 h-16 bg-blue-500 rounded-full animate-pulse"></div>
            </div> 
        }>
            <Card className="m-0 p-0 bg-secondary">
                <CardBody className="mt-4 grid place-items-center px-2">
                    <Chart {...chartConfig} />
                </CardBody>
            </Card>
        </Suspense>
        </>
    )
}

export default GenresPieChart