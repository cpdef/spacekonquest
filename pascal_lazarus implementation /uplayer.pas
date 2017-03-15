unit uPlayer;

{$mode objfpc}{$H+}

interface

uses
  Graphics, Classes, SysUtils;

type TPlayer = class
  color: tcolor;
  ID: integer;
  iski: boolean;
  procedure new_color();
  constructor create(new_id: integer; new_iski:boolean);
end;

implementation

procedure TPlayer.new_color();
var cRed, cGreen, cBlue: integer;
begin
   repeat
   cRed:=Random(200);
   cGreen:=Random(200);
   cBlue:=Random(200);
   until abs(cBlue-cGreen) >= 100;
   color:=RGBToColor(cRed, cGreen, cBlue);
end;

constructor TPlayer.create(new_id: integer, new_iski:boolean);
begin
   ID := new_id;
   new_color();
end;

end.

