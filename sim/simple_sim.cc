// DESCRIPTION: Verilator: Verilog example module
//
// This file ONLY is placed under the Creative Commons Public Domain, for
// any use, without warranty, 2017 by Wilson Snyder.
// SPDX-License-Identifier: CC0-1.0
//======================================================================

// For std::unique_ptr
#include <memory>

// Include common routines
#include <verilated.h>

// Include model header, generated from Verilating "ibex_super_system.v"
#include "Vibex_super_system.h"

// Legacy function required only so linking works on Cygwin and MSVC++
// double sc_time_stamp() { return 0; }

// #define CLKS 100000000
#define CLKS 1000000
// #define CLKS 60000000

int main(int argc, char** argv, char** env) {
    // This is a more complicated example, please also see the simpler examples/make_hello_c.

    // Prevent unused variable warnings
    if (false && argc && argv && env) {}

    // Create logs/ directory in case we have traces to put under it
    Verilated::mkdir("logs");

    // Construct a VerilatedContext to hold simulation time, etc.
    // Multiple modules (made later below with Vibex_super_system) may share the same
    // context to share time, or modules may have different contexts if
    // they should be independent from each other.

    // Using unique_ptr is similar to
    // "VerilatedContext* contextp = new VerilatedContext" then deleting at end.
    const std::unique_ptr<VerilatedContext> contextp{new VerilatedContext};

    // Set debug level, 0 is off, 9 is highest presently used
    // May be overridden by commandArgs argument parsing
    contextp->debug(0);

    // Randomization reset policy
    // May be overridden by commandArgs argument parsing
    contextp->randReset(2);

    // Verilator must compute traced signals
    contextp->traceEverOn(true);

    // Pass arguments so Verilated code can see them, e.g. $value$plusargs
    // This needs to be called before you create any model
    contextp->commandArgs(argc, argv);

    // Construct the Verilated model, from Vibex_super_system.h generated from Verilating "ibex_super_system.v".
    // Using unique_ptr is similar to "Vibex_super_system* ibex_super_system = new Vibex_super_system" then deleting at end.
    // "TOP" will be the hierarchical name of the module.
    const std::unique_ptr<Vibex_super_system> ibex_super_system{new Vibex_super_system{contextp.get(), "TOP"}};

    // Set Vibex_super_system's input signals
    // ibex_super_system->reset_l = !0;
    // ibex_super_system->clk = 0;
    // ibex_super_system->in_small = 1;
    // ibex_super_system->in_quad = 0x1234;
    // ibex_super_system->in_wide[0] = 0x11111111;
    // ibex_super_system->in_wide[1] = 0x22222222;
    // ibex_super_system->in_wide[2] = 0x3;
    ibex_super_system->clk_sys_i = 0;
    ibex_super_system->rst_sys_ni = !0;
    ibex_super_system->uart_rx_i = 1;

    // Simulate until $finish
    while (!contextp->gotFinish() && contextp->time() < 2*CLKS) {
        // Historical note, before Verilator 4.200 Verilated::gotFinish()
        // was used above in place of contextp->gotFinish().
        // Most of the contextp-> calls can use Verilated:: calls instead;
        // the Verilated:: versions just assume there's a single context
        // being used (per thread).  It's faster and clearer to use the
        // newer contextp-> versions.

        contextp->timeInc(1);  // 1 timeprecision period passes...
        // Historical note, before Verilator 4.200 a sc_time_stamp()
        // function was required instead of using timeInc.  Once timeInc()
        // is called (with non-zero), the Verilated libraries assume the
        // new API, and sc_time_stamp() will no longer work.

        // Toggle a fast (time/2 period) clock
        ibex_super_system->clk_sys_i = !ibex_super_system->clk_sys_i;

        // Toggle control signals on an edge that doesn't correspond
        // to where the controls are sampled; in this example we do
        // this only on a negedge of clk, because we know
        // reset is not sampled there.
        if (!ibex_super_system->clk_sys_i) {
            if (contextp->time() > 1 && contextp->time() < 10) {
                ibex_super_system->rst_sys_ni = !1;  // Assert reset
            } else {
                ibex_super_system->rst_sys_ni = !0;  // Deassert reset
            }
            // Assign some other inputs
            // ibex_super_system->in_quad += 0x12;
            if (contextp->time() < 151000) {
                ibex_super_system->uart_rx_i = 1;
            }
            else if (contextp->time() < 151868) {
                ibex_super_system->uart_rx_i = 0;
            }
            
            else if (contextp->time() < 171000) {
                ibex_super_system->uart_rx_i = 1;
            }
            else if (contextp->time() < 171868) {
                ibex_super_system->uart_rx_i = 0;
            }

            else if (contextp->time() < 191000) {
                ibex_super_system->uart_rx_i = 1;
            }
            else if (contextp->time() < 191868) {
                ibex_super_system->uart_rx_i = 0;
            }

            else if (contextp->time() < 211000) {
                ibex_super_system->uart_rx_i = 1;
            }
            else if (contextp->time() < 211868) {
                ibex_super_system->uart_rx_i = 0;
            }

            else if (contextp->time() < 231000) {
                ibex_super_system->uart_rx_i = 1;
            }
            else if (contextp->time() < 231868) {
                ibex_super_system->uart_rx_i = 0;
            }

            else if (contextp->time() < 251000) {
                ibex_super_system->uart_rx_i = 1;
            }
            else if (contextp->time() < 251868) {
                ibex_super_system->uart_rx_i = 0;
            }

            else if (contextp->time() < 271000) {
                ibex_super_system->uart_rx_i = 1;
            }
            else if (contextp->time() < 271868) {
                ibex_super_system->uart_rx_i = 0;
            }

            else {
                ibex_super_system->uart_rx_i = 1;
            }
        }



        // Evaluate model
        // (If you have multiple models being simulated in the same
        // timestep then instead of eval(), call eval_step() on each, then
        // eval_end_step() on each. See the manual.)
        ibex_super_system->eval();

        // Read outputs
        // VL_PRINTF("[%" PRId64 "] clk=%x rstl=%x iquad=%" PRIx64 " -> oquad=%" PRIx64
        //           " owide=%x_%08x_%08x\n",
        //           contextp->time(), ibex_super_system->clk, ibex_super_system->reset_l, ibex_super_system->in_quad, ibex_super_system->out_quad,
        //           ibex_super_system->out_wide[2], ibex_super_system->out_wide[1], ibex_super_system->out_wide[0]);
        // VL_PRINTF("[%" PRId64 "] clk=%x rstl=%x \n",
        //           contextp->time(), ibex_super_system->clk_sys_i, ibex_super_system->rst_sys_ni);
    }

    // Final model cleanup
    ibex_super_system->final();

    // Coverage analysis (calling write only after the test is known to pass)
// #if VM_COVERAGE
//     Verilated::mkdir("logs");
//     contextp->coveragep()->write("logs/coverage.dat");
// #endif

    // Return good completion status
    // Don't use exit() or destructor won't get called
    return 0;
}