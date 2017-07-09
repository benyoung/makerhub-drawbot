mm=1;
in=25.4*mm;


slop = 0.3*mm;
pen_rad = 8.66*mm+slop;
pen_height = 0.5*in;

wall = 3*mm;
eps=0.01*mm;

num_ribs=7;

motor_hole_rad = 0.9*mm;
motor_hole_y = pen_rad+wall-2.2*mm;
motor_hole_z = 5.75*mm;

module pen_tube() {
    union(){
        difference(){
            union() {
                cylinder(r=pen_rad+wall, h=pen_height);
                cube([pen_rad+wall, pen_rad+wall, pen_height]);

            }
            union() {
                translate([0,0,-eps])
                cylinder(r=pen_rad, h=pen_height+2*eps);
                
                                
                color("red")
                translate([0,motor_hole_y, motor_hole_z])
                rotate([0,90,0])
                cylinder(r=motor_hole_rad, h=2*pen_height,  $fn=16);
            }
        }
        for(i=[0:num_ribs-1]){
            rotate(360/num_ribs*i)
            translate([pen_rad,0,0])
            cylinder(r=slop,h=pen_height,$fn=2*num_ribs);
        }
    }
}

pen_tube();


