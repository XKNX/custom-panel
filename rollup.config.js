import {terser} from "rollup-plugin-terser";
import cleanup from "rollup-plugin-cleanup";
import commonjs from "@rollup/plugin-commonjs";
import dev from "rollup-plugin-dev";
import json from "@rollup/plugin-json";
import nodeResolve from "@rollup/plugin-node-resolve";
import progress from "rollup-plugin-progress";
import sizes from "rollup-plugin-sizes";
import typescript from "rollup-plugin-typescript2";

const isdev = process.env.ROLLUP_WATCH;

const Plugins = [
    progress(),
    nodeResolve(),
    commonjs(),
    typescript(),
    json({
        compact: true,
        preferConst: true,
    }),
    !isdev && terser({}),
    !isdev && cleanup({
        comments: "none",
    }),
    isdev && sizes(),
    isdev && sizes({
        details: true,
    }),
    isdev && dev({
        dirs: ["../"],
        port: 5000,
        host: "0.0.0.0",
    }),
];

export default [
    {
        watch: {
            chokidar: {
                usePolling: true,
            },
        },
        input: ["src/knx_ui.ts"],
        output: {
            file: `./xknx-custom-panel/knx_ui.js`,
            name: "knx_ui.js",
            format: "iife",
        },
        plugins: [...Plugins],
    },
];
