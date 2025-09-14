// magic.v
// Core transformation module for the Verilog Flag Checker challenge

module magic(
    input  wire        clk,
    input  wire        rst,
    input  wire [7:0]  inp,
    input  wire [1:0]  val,
    output reg  [7:0]  res
);
    always @(*) begin
        case (val)
            2'b00: res = ((inp << 3) | (inp >> 5)) & 8'hFF;       // rotate left by 3
            2'b01: res = ((inp >> 2) ^ 8'h5A) & 8'hFF;            // shift right 2, XOR with 0x5A
            2'b10: res = (inp + 8'd77) & 8'hFF;                   // add 77
            2'b11: res = (inp ^ 8'h33) & 8'hFF;                   // XOR with 0x33
            default: res = inp;
        endcase
    end
endmodule
