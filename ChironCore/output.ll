; ModuleID = 'Chiron Module'
source_filename = "Chiron Module"

@fmt = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@fmt.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@fmt.2 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@fmt.3 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@fmt.4 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@fmt.5 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@fmt.6 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@fmt.7 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1

declare i32 @printf(ptr, ...)

declare void @init()

declare void @handleGoTo(i32, i32)

declare void @handleForward(i32)

declare void @handleBackward(i32)

declare void @handleRight(i32)

declare void @handleLeft(i32)

declare void @handlePenUp()

declare void @handlePenDown()

declare void @finish()

define i32 @main() {
entry:
  %__rep_counter_1 = alloca i32, align 4
  %":steps" = alloca i32, align 4
  %":p" = alloca i32, align 4
  %":z" = alloca i32, align 4
  %":y" = alloca i32, align 4
  %":x" = alloca i32, align 4
  call void @init()
  %prnt = call i32 (ptr, ...) @printf(ptr @fmt, i32 20)
  store i32 20, ptr %":x", align 4
  %prnt1 = call i32 (ptr, ...) @printf(ptr @fmt.1, i32 30)
  store i32 30, ptr %":y", align 4
  %prnt2 = call i32 (ptr, ...) @printf(ptr @fmt.2, i32 20)
  store i32 20, ptr %":z", align 4
  %prnt3 = call i32 (ptr, ...) @printf(ptr @fmt.3, i32 40)
  store i32 40, ptr %":p", align 4
  %prnt4 = call i32 (ptr, ...) @printf(ptr @fmt.4, i32 3)
  store i32 3, ptr %":steps", align 4
  call void @handlePenDown()
  %":steps5" = load i32, ptr %":steps", align 4
  store i32 %":steps5", ptr %__rep_counter_1, align 4
  br label %loop

loop:                                             ; preds = %ifcont22, %entry
  %":x6" = load i32, ptr %":x", align 4
  %":y7" = load i32, ptr %":y", align 4
  %gttmp = icmp sgt i32 %":x6", %":y7"
  br i1 %gttmp, label %then, label %else

then:                                             ; preds = %loop
  %":x8" = load i32, ptr %":x", align 4
  %":y9" = load i32, ptr %":y", align 4
  %":x10" = load i32, ptr %":x", align 4
  call void @drawRectangle(i32 %":x8", i32 %":y9", i32 %":x10")
  br label %ifcont

else:                                             ; preds = %loop
  %":y11" = load i32, ptr %":y", align 4
  %":x12" = load i32, ptr %":x", align 4
  %":p13" = load i32, ptr %":p", align 4
  call void @drawPentagon(i32 %":y11", i32 %":x12", i32 %":p13")
  br label %ifcont

ifcont:                                           ; preds = %else, %then
  %":z14" = load i32, ptr %":z", align 4
  %":p15" = load i32, ptr %":p", align 4
  %gtetmp = icmp sge i32 %":z14", %":p15"
  br i1 %gtetmp, label %then16, label %else21

then16:                                           ; preds = %ifcont
  %":p17" = load i32, ptr %":p", align 4
  %":x18" = load i32, ptr %":x", align 4
  %":z19" = load i32, ptr %":z", align 4
  %addtmp = add i32 %":x18", %":z19"
  %":x20" = load i32, ptr %":x", align 4
  call void @drawHexagon(i32 %":p17", i32 %addtmp, i32 %":x20")
  br label %ifcont22

else21:                                           ; preds = %ifcont
  br label %ifcont22

ifcont22:                                         ; preds = %else21, %then16
  %":x23" = load i32, ptr %":x", align 4
  %addtmp24 = add i32 %":x23", 10
  %prnt25 = call i32 (ptr, ...) @printf(ptr @fmt.5, i32 %addtmp24)
  store i32 %addtmp24, ptr %":x", align 4
  %":y26" = load i32, ptr %":y", align 4
  %addtmp27 = add i32 %":y26", 10
  %prnt28 = call i32 (ptr, ...) @printf(ptr @fmt.6, i32 %addtmp27)
  store i32 %addtmp27, ptr %":y", align 4
  %":z29" = load i32, ptr %":z", align 4
  %addtmp30 = add i32 %":z29", 10
  %prnt31 = call i32 (ptr, ...) @printf(ptr @fmt.7, i32 %addtmp30)
  store i32 %addtmp30, ptr %":z", align 4
  %__rep_counter_132 = load i32, ptr %__rep_counter_1, align 4
  %nextvar = sub i32 %__rep_counter_132, 1
  store i32 %nextvar, ptr %__rep_counter_1, align 4
  %loopcond = icmp ne i32 %nextvar, 0
  br i1 %loopcond, label %loop, label %afterloop

afterloop:                                        ; preds = %ifcont22
  call void @handlePenUp()
  call void @finish()
  ret i32 0
}

define void @drawRectangle(i32 %":x", i32 %":y", i32 %":len") {
entry:
  %__rep_counter_1 = alloca i32, align 4
  %":len3" = alloca i32, align 4
  %":y2" = alloca i32, align 4
  %":x1" = alloca i32, align 4
  store i32 %":x", ptr %":x1", align 4
  store i32 %":y", ptr %":y2", align 4
  store i32 %":len", ptr %":len3", align 4
  call void @handlePenUp()
  %":x4" = load i32, ptr %":x1", align 4
  %":y5" = load i32, ptr %":y2", align 4
  call void @handleGoTo(i32 %":x4", i32 %":y5")
  call void @handlePenDown()
  store i32 4, ptr %__rep_counter_1, align 4
  br label %loop

loop:                                             ; preds = %loop, %entry
  %":len6" = load i32, ptr %":len3", align 4
  call void @handleForward(i32 %":len6")
  call void @handleLeft(i32 90)
  %__rep_counter_17 = load i32, ptr %__rep_counter_1, align 4
  %nextvar = sub i32 %__rep_counter_17, 1
  store i32 %nextvar, ptr %__rep_counter_1, align 4
  %loopcond = icmp ne i32 %nextvar, 0
  br i1 %loopcond, label %loop, label %afterloop

afterloop:                                        ; preds = %loop
  ret void
}

define void @drawPentagon(i32 %":x", i32 %":y", i32 %":len") {
entry:
  %__rep_counter_1 = alloca i32, align 4
  %":len3" = alloca i32, align 4
  %":y2" = alloca i32, align 4
  %":x1" = alloca i32, align 4
  store i32 %":x", ptr %":x1", align 4
  store i32 %":y", ptr %":y2", align 4
  store i32 %":len", ptr %":len3", align 4
  call void @handlePenUp()
  %":x4" = load i32, ptr %":x1", align 4
  %":y5" = load i32, ptr %":y2", align 4
  call void @handleGoTo(i32 %":x4", i32 %":y5")
  call void @handlePenDown()
  store i32 5, ptr %__rep_counter_1, align 4
  br label %loop

loop:                                             ; preds = %loop, %entry
  %":len6" = load i32, ptr %":len3", align 4
  call void @handleForward(i32 %":len6")
  call void @handleLeft(i32 72)
  %__rep_counter_17 = load i32, ptr %__rep_counter_1, align 4
  %nextvar = sub i32 %__rep_counter_17, 1
  store i32 %nextvar, ptr %__rep_counter_1, align 4
  %loopcond = icmp ne i32 %nextvar, 0
  br i1 %loopcond, label %loop, label %afterloop

afterloop:                                        ; preds = %loop
  ret void
}

define void @drawHexagon(i32 %":x", i32 %":y", i32 %":len") {
entry:
  %__rep_counter_1 = alloca i32, align 4
  %":len3" = alloca i32, align 4
  %":y2" = alloca i32, align 4
  %":x1" = alloca i32, align 4
  store i32 %":x", ptr %":x1", align 4
  store i32 %":y", ptr %":y2", align 4
  store i32 %":len", ptr %":len3", align 4
  call void @handlePenUp()
  %":x4" = load i32, ptr %":x1", align 4
  %":y5" = load i32, ptr %":y2", align 4
  call void @handleGoTo(i32 %":x4", i32 %":y5")
  call void @handlePenDown()
  store i32 6, ptr %__rep_counter_1, align 4
  br label %loop

loop:                                             ; preds = %loop, %entry
  %":len6" = load i32, ptr %":len3", align 4
  call void @handleBackward(i32 %":len6")
  call void @handleLeft(i32 60)
  %__rep_counter_17 = load i32, ptr %__rep_counter_1, align 4
  %nextvar = sub i32 %__rep_counter_17, 1
  store i32 %nextvar, ptr %__rep_counter_1, align 4
  %loopcond = icmp ne i32 %nextvar, 0
  br i1 %loopcond, label %loop, label %afterloop

afterloop:                                        ; preds = %loop
  ret void
}
