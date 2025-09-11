'use client'

import {
    Card,
    CardBody
} from "@material-tailwind/react";
import dynamic from "next/dynamic";
import { Suspense, useState } from "react";

type Props = {
    genres: [string, number][],
    callback: (genre: string | null) => void
}

const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

const GenresPieChart = ({genres, callback}: Props) => {
    const [prev, setPrev] = useState<string | null>(null)
    const type = "pie" as const;
    const themeMode = "dark" as const;
    const chartConfig = {
        type: type,
        series: genres.map((arr:[string, number])=>(
            arr[1]
        )),
        options: {
            theme: {
                mode: themeMode,
            },
            chart: {
                events: {
                    dataPointSelection: function(event: object, chartContext: object, config: { w: { config: { labels: { [x: string]: string; }; }; }; dataPointIndex: string | number; }) {
                      // Get the label name
                      const clickedValue = config.w.config.labels[config.dataPointIndex];
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
            <Card className="m-0 p-0 bg-secondary" placeholder={undefined} onResize={undefined} onResizeCapture={undefined} onPointerEnterCapture={undefined} onPointerLeaveCapture={undefined}>
                <CardBody className="mt-4 grid place-items-center px-2" placeholder={undefined} onResize={undefined} onResizeCapture={undefined} onPointerEnterCapture={undefined} onPointerLeaveCapture={undefined}>
                    <Chart {...chartConfig} />
                </CardBody>
            </Card>
        </Suspense>
        </>
    )
}

export default GenresPieChart