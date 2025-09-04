`timescale 1ns/10ps

`include "./chall.v"

module t_chall();
  reg clk, rst, ok;
  reg[7:0] inp, idx, tmp;
  wire[7:0] out;
  wire[7:0] target[25:0];   // 26 targets

  // replace this with the generated target values
  assign {target[0], target[1], target[2], target[3], target[4], target[5],
          target[6], target[7], target[8], target[9], target[10], target[11],
          target[12], target[13], target[14], target[15], target[16], target[17],
          target[18], target[19], target[20], target[21], target[22], target[23],
          target[24], target[25]} =
          {8'd77, 8'd105, 8'd111, 8'd105, 8'd74, 8'd106, 8'd115, 8'd10, 
           8'd249, 8'd10, 8'd73, 8'd106, 8'd125, 8'd10, 8'd125, 8'd73, 
           8'd111, 8'd249, 8'd74, 8'd73, 8'd106, 8'd249, 8'd68, 8'd111, 
           8'd125, 8'd75};

  chall ch(.clk(clk), .rst(rst), .inp(inp), .res(out));

  initial begin
    $dumpfile("chall.vcd");
    $dumpvars;

    clk = 1'b0;
    #1 rst = 1'b1;
    #1 rst = 1'b0;

    ok = 1'b1;
    for (idx = 0; idx < 26; idx++) begin
      inp = target[idx];   // feed each target
      tmp = target[idx];   // expected output is target
      #4;
    end

    if (ok) begin
      $display("ok");
    end else begin
      $display("no");
    end

    $finish;
  end

  always @(posedge clk) begin
    #1 ok = ok & (out == tmp);
  end

  always begin
    #2 clk = ~clk;
  end
endmodule