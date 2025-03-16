; ModuleID = 'Chiron Module'
source_filename = "Chiron Module"

@fmt = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@fmt.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@fmt.2 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@fmt.3 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@fmt.4 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@fmt.5 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@fmt.6 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1

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
  %__rep_counter_2 = alloca i32, align 4
  %__rep_counter_1 = alloca i32, align 4
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
  call void @handlePenDown()
  store i32 3, ptr %__rep_counter_1, align 4
  br label %loop

loop:                                             ; preds = %ifcont32, %entry
  %":x4" = load i32, ptr %":x", align 4
  %":y5" = load i32, ptr %":y", align 4
  %gttmp = icmp sgt i32 %":x4", %":y5"
  br i1 %gttmp, label %then, label %else

then:                                             ; preds = %loop
  call void @handlePenUp()
  %":x6" = load i32, ptr %":x", align 4
  %":y7" = load i32, ptr %":y", align 4
  call void @handleGoTo(i32 %":x6", i32 %":y7")
  call void @handlePenDown()
  store i32 4, ptr %__rep_counter_2, align 4
  br label %loop8

loop8:                                            ; preds = %loop8, %then
  %":x9" = load i32, ptr %":x", align 4
  call void @handleForward(i32 %":x9")
  call void @handleLeft(i32 90)
  %__rep_counter_210 = load i32, ptr %__rep_counter_2, align 4
  %nextvar = sub i32 %__rep_counter_210, 1
  store i32 %nextvar, ptr %__rep_counter_2, align 4
  %loopcond = icmp ne i32 %nextvar, 0
  br i1 %loopcond, label %loop8, label %afterloop

afterloop:                                        ; preds = %loop8
  br label %ifcont

else:                                             ; preds = %loop
  call void @handlePenUp()
  %":y11" = load i32, ptr %":y", align 4
  %":x12" = load i32, ptr %":x", align 4
  call void @handleGoTo(i32 %":y11", i32 %":x12")
  call void @handlePenDown()
  store i32 5, ptr %__rep_counter_2, align 4
  br label %loop13

loop13:                                           ; preds = %loop13, %else
  %":p14" = load i32, ptr %":p", align 4
  call void @handleForward(i32 %":p14")
  call void @handleLeft(i32 72)
  %__rep_counter_215 = load i32, ptr %__rep_counter_2, align 4
  %nextvar16 = sub i32 %__rep_counter_215, 1
  store i32 %nextvar16, ptr %__rep_counter_2, align 4
  %loopcond17 = icmp ne i32 %nextvar16, 0
  br i1 %loopcond17, label %loop13, label %afterloop18

afterloop18:                                      ; preds = %loop13
  br label %ifcont

ifcont:                                           ; preds = %afterloop18, %afterloop
  %":z19" = load i32, ptr %":z", align 4
  %":p20" = load i32, ptr %":p", align 4
  %gtetmp = icmp sge i32 %":z19", %":p20"
  br i1 %gtetmp, label %then21, label %else31

then21:                                           ; preds = %ifcont
  call void @handlePenUp()
  %":p22" = load i32, ptr %":p", align 4
  %":x23" = load i32, ptr %":x", align 4
  %":z24" = load i32, ptr %":z", align 4
  %addtmp = add i32 %":x23", %":z24"
  call void @handleGoTo(i32 %":p22", i32 %addtmp)
  call void @handlePenDown()
  store i32 6, ptr %__rep_counter_2, align 4
  br label %loop25

loop25:                                           ; preds = %loop25, %then21
  %":x26" = load i32, ptr %":x", align 4
  call void @handleBackward(i32 %":x26")
  call void @handleLeft(i32 60)
  %__rep_counter_227 = load i32, ptr %__rep_counter_2, align 4
  %nextvar28 = sub i32 %__rep_counter_227, 1
  store i32 %nextvar28, ptr %__rep_counter_2, align 4
  %loopcond29 = icmp ne i32 %nextvar28, 0
  br i1 %loopcond29, label %loop25, label %afterloop30

afterloop30:                                      ; preds = %loop25
  br label %ifcont32

else31:                                           ; preds = %ifcont
  br label %ifcont32

ifcont32:                                         ; preds = %else31, %afterloop30
  %":x33" = load i32, ptr %":x", align 4
  %addtmp34 = add i32 %":x33", 10
  %prnt35 = call i32 (ptr, ...) @printf(ptr @fmt.4, i32 %addtmp34)
  store i32 %addtmp34, ptr %":x", align 4
  %":y36" = load i32, ptr %":y", align 4
  %addtmp37 = add i32 %":y36", 10
  %prnt38 = call i32 (ptr, ...) @printf(ptr @fmt.5, i32 %addtmp37)
  store i32 %addtmp37, ptr %":y", align 4
  %":z39" = load i32, ptr %":z", align 4
  %addtmp40 = add i32 %":z39", 10
  %prnt41 = call i32 (ptr, ...) @printf(ptr @fmt.6, i32 %addtmp40)
  store i32 %addtmp40, ptr %":z", align 4
  %__rep_counter_142 = load i32, ptr %__rep_counter_1, align 4
  %nextvar43 = sub i32 %__rep_counter_142, 1
  store i32 %nextvar43, ptr %__rep_counter_1, align 4
  %loopcond44 = icmp ne i32 %nextvar43, 0
  br i1 %loopcond44, label %loop, label %afterloop45

afterloop45:                                      ; preds = %ifcont32
  call void @handlePenUp()
  call void @finish()
  ret i32 0
}
