mm = 1; 

slop = 0.5*mm;
ribs=10;

$fn=30;
stepper_rad = 14.1*mm+slop;
stepper_height = 19*mm;
wall = 2*mm;
width = (stepper_rad+wall)*2;

wiring_cutout = 18*mm;
wiring_depth = 3*mm;
wiring_height = 14*mm; // made-up number
pin_inset = 3*mm;
pin_rad = 0.4*mm;
eps=0.01;

hole_offset = 17.5*mm; // made-up number
hole_rad = 1.5*mm; // made_up_number
hole_outer_rad = hole_rad+wall;

module motor_block() {
    union() {
        for(rib=[1:ribs-2]) {
            rotate([0,0,360/ribs * (rib-1)+138])
            
            translate([stepper_rad,0,0])
            cylinder(r=slop, h=stepper_height);
        }
        
        difference() {
            union() {
                translate([-width/2,-width/2,0])
                cube([width, wall+2*stepper_rad+wiring_depth, stepper_height]);
                
                translate([-width/2,stepper_rad+wiring_depth,0])
                cube([width, wall, wiring_height]);
                
                for(side = [-1,1]){
                    translate([side*hole_offset,0,0])
                    cylinder(r=hole_outer_rad,h=stepper_height);
                    translate([side*(hole_offset-hole_outer_rad/2),0,0])
                    translate([-hole_outer_rad/2,-hole_outer_rad,0])
                    cube([hole_outer_rad,2*hole_outer_rad,stepper_height]);
                }
                
            }
            union() {
                translate([0,0,-eps])
                cylinder(r=stepper_rad, h=stepper_height+2*eps);
                
                
                color("red")
                translate([-wiring_cutout/2,0,-eps])
                cube([wiring_cutout,stepper_rad+wiring_depth+eps,stepper_height+2*eps]);
                for(side = [-1,1]){
                    translate([side*hole_offset,0,-eps])
                    cylinder(r=hole_rad,h=stepper_height+2*eps);
                }
            }
        }
    }
}





eyelet_x = 55*mm;
eyelet_y = 8*mm;
pin_x = [21*mm, 44*mm, eyelet_x];
pin_y = [48*mm, 30*mm, eyelet_y];
pin_rad = 1.0*mm;
pin_plinth_rad= 5*mm;
pin_plinth_height=4*mm;
plate_th=2*mm;

plate_y = 66.5*mm;
plate_x = eyelet_x + pin_plinth_rad;

motor_block_inset = 4.5*mm;

tab_width = 4.2*mm;
plate_points = [
    [0,0], 
    [0,plate_y], 
    [width, plate_y], 
    [eyelet_x+pin_plinth_rad, eyelet_y],
    [eyelet_x+pin_plinth_rad,0],
    [0,0]
];


module motor_mount() {
    difference(){
        union(){
                    
            color("green")
            linear_extrude(height=plate_th) 
            intersection(){
                polygon(plate_points);
                circle(r=plate_y, $fn=120);
            }
            translate([width/2 + motor_block_inset, width/2 + tab_width, plate_th-eps])
            motor_block();
            for(i=[0:2]) {
                translate([pin_x[i], pin_y[i], 0])
                cylinder(r=pin_plinth_rad, h=pin_plinth_height);
            }
        }
        union(){
            for(i=[0:2]) {
                translate([pin_x[i], pin_y[i], -eps])
                cylinder(r=pin_rad, h=pin_plinth_height+2*eps);
            }
        }
    }
}

motor_mount();




