with Ada.Text_IO, Ada.Integer_Text_IO;
use Ada.Text_IO, Ada.Integer_Text_IO;

procedure Proced2 is

   Counter1 : INTEGER:=6;
   Counter2 : INTEGER:=1;
   --Counter3 : INTEGER:=5;

   procedure putf(n : in Integer) is
	begin
		Print(n);
		Print_Newline(1);
	end putf;
   
   
begin
   --Counter3:= 2;
   Counter2:= 'a';
   Print_Newline(1);
   Print(Counter1);
   Print_Newline(1);
   Print(Counter2);
   
end Proced2;
