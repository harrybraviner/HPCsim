%This script is very messy but was used to generate diffusion and advection results which were saved and then loaded on future runs.
%These results were then plotted and saved as a movie/gif files.

%This was written after 9pm the evening before the presentations so no guarantee is made about code quality, accuracy or documentation.

clear
load diffusion
%[~, u1] = runSimulation(1,0,0,1,150);
%[~, u4] = runSimulation(4,0,0,1,150);
%[x, u20] = runSimulation(20,0,0,1,150);


%load advection
%a = -0.002;
%[~, u1] = runSimulation(1,a,0,0,150);
%[~, u4] = runSimulation(4,a,0,0,150);
%[x, u20] = runSimulation(20,a,0,0,150);
%save advection


%load advection2
%a = 0.01;
%[~, u1] = runSimulation(1,0,a,0,150);
%[~, u4] = runSimulation(4,0,a,0,150);
%[x, u20] = runSimulation(20,0,a,0,150);
%save advection2


%# figure

%# preallocate
nFrames = 30;
%mov(1:nFrames) = struct('cdata',[], 'colormap',[]);

%# create movie

figure, set(gcf, 'Color','white')
k=1;
plot(x, u20(k,:), 'g', x,u4(k,:),'r',x,u1(k,:), 'b', 'LineWidth', 2);  axis tight
title('Central difference diffusion equation');
legend('Twenty computational nodes', 'Four computational nodes', 'One computational node');
SP=x(25); %your point goes here
line([SP SP],get(gca,'YLim'),'Color','k', 'LineWidth', 0.5)
SP=x(5); %your point goes here
line([SP SP],get(gca,'YLim'),'Color','k', 'LineWidth', 0.5)

f = getframe(gca);
[f,map] = rgb2ind(f.cdata, 256, 'nodither');
mov = repmat(f, [1 1 1 nFrames]);

for k=1:nFrames
    plot(x, u20(k,:), 'g', x,u4(k,:),'r',x,u1(k,:), 'b', 'LineWidth', 2);  axis tight
    title('Central difference diffusion equation');
    legend('Twenty computational nodes', 'Four computational nodes', 'One computational node');

    %Plot vertical lines 
   
    SP=x(25); %your point goes here
    line([SP SP],get(gca,'YLim'),'Color','k', 'LineWidth', 0.5)
    
    SP=x(5); %your point goes here
    line([SP SP],get(gca,'YLim'),'Color','k', 'LineWidth', 0.5)
   
    f = getframe(gca);
    mov(:,:,1,k) = rgb2ind(f.cdata, map, 'nodither');;
end
close(gcf)


imwrite(mov, map, 'advection2.gif', 'DelayTime',0.4, 'LoopCount',inf)
%# save as AVI file, and open it using system video player
%movie2avi(mov, 'advection.avi', 'compression','None', 'fps',10);
