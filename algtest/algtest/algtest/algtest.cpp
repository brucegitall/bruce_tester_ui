#include "algtest.h"


struct bruce_info {
    vector<Point2i> points;
};





algtest::algtest ( QWidget *parent )
    : QMainWindow ( parent )
{
    ui.setupUi ( this );

    m_signalMapper_basic = new QSignalMapper();

    m_image_folder = "F:\\Bruce\\Qt_Pgm\\images\\";
    m_imageDir_basic = new QDir ( m_image_folder );
    m_imageDir_basic->setFilter ( QDir::Files );

    m_plot = new QCustomPlot ( );
    m_plot->show();
    ui.plotLayout->addWidget ( m_plot );

    ui.label_img->setScaledContents ( true );

    connect ( ui.button_reflash, &QPushButton::clicked, this, &algtest::OnReflashImages );

    connect ( ui.combox_images, static_cast<void ( QComboBox::* ) ( const QString & ) > ( &QComboBox::currentIndexChanged ), this, &algtest::OnChangeImage );
    // add code here



    connect ( ui.button_hsv, &QPushButton::clicked, m_signalMapper_basic, static_cast<void ( QSignalMapper::* ) () > ( &QSignalMapper::map ) );
    m_signalMapper_basic->setMapping ( ui.button_hsv,"HSV_TEST" );



    // don't change this line
    connect ( m_signalMapper_basic, static_cast<void ( QSignalMapper::* ) ( const QString & ) > ( &QSignalMapper::mapped ), this, &algtest::OnMapperMessages );

}

algtest::~algtest()
{

}


void algtest::Mat2QImage ( QImage & qImg, Mat cvImg )
{
    if ( cvImg.channels() == 3 ) {                         //3 channels color image

        cvtColor ( cvImg, cvImg, CV_BGR2RGB );
        qImg = QImage ( ( const unsigned char* ) ( cvImg.data ),
                        cvImg.cols, cvImg.rows,
                        cvImg.cols*cvImg.channels(),
                        QImage::Format_RGB888 );
    }
    else if ( cvImg.channels() == 1 ) {                //grayscale image
        qImg = QImage ( ( const unsigned char* ) ( cvImg.data ),
                        cvImg.cols, cvImg.rows,
                        cvImg.cols*cvImg.channels(),
                        QImage::Format_Indexed8 );
    }
    else {
        qImg = QImage ( ( const unsigned char* ) ( cvImg.data ),
                        cvImg.cols, cvImg.rows,
                        cvImg.cols*cvImg.channels(),
                        QImage::Format_RGB888 );
    }

}


void algtest::draw_line ( QVector<double> & x, QVector<double> & y )
{
    // create graph and assign data to it:
    QPen pen;
    pen.setStyle ( Qt::DotLine );

    m_plot->addGraph();
    m_plot->graph ( 0 )->setData ( x, y );
    m_plot->graph ( 0 )->setPen ( pen );
    // give the axes some labels:
    m_plot->graph ( 0 )->setName ( QString ( "ÇúÏß1" ) );
    m_plot->xAxis->setLabel ( "x" );
    m_plot->yAxis->setLabel ( "y" );
    // set axes ranges, so we see all data:
    m_plot->xAxis->setRange ( x.first(),x.last() );
    QVector<double> y_sort = y;
    std::sort ( y_sort.begin(), y_sort.end() );
    m_plot->yAxis->setRange ( y_sort.first() - 1, y_sort.last() +1 );




    m_plot->replot();
}

void algtest::OnReflashImages()
{
    m_imageDir_basic->refresh();
    ui.combox_images->clear();
    ui.combox_images->addItems ( m_imageDir_basic->entryList() );

}
void algtest::OnChangeImage ( const QString & key )
{
    m_image_name = ui.combox_images->currentText();
    Mat img_rgb = imread ( ( m_image_folder + m_image_name ).toStdString() );
    display_img ( img_rgb );
}
void algtest::display_img ( Mat & img_rgb )
{
    QImage qimage;
    Mat2QImage ( qimage, img_rgb );
    qimage.scaled ( ui.label_img->width(), ui.label_img->height() );
    ui.label_img->setPixmap ( QPixmap::fromImage ( qimage ) );
}
void algtest::OnMapperMessages ( const QString &  key )
{
    if ( QString::compare ( "HSV_TEST", key ) == 0 ) {

        Mat img_rgb = imread ( ( m_image_folder + m_image_name ).toStdString() );

        int img_width = img_rgb.cols;
        int img_height = img_rgb.rows;


        Mat img_hsv;
        img_hsv.create ( img_height, img_width,CV_8UC3 );

        cvtColor ( img_rgb, img_hsv, CV_RGB2HSV );
        vector<Mat> hsv_vec;
        split ( img_hsv, hsv_vec );
        if ( hsv_vec.size() >0 ) {
            Mat img_h = hsv_vec[0];
            Mat img_s = hsv_vec[1];
            Mat img_v = hsv_vec[2];

            display_img ( img_h );

            //vector<bruce_info> infos;
            QMap<int, vector<Point2i>> infos;


            for ( int k=0; k < 180; k++ ) {
                infos[k] = vector<Point2i>();
            }

            for ( int i = 0; i < img_height; i++ ) {
                const uchar* img_data = img_h.ptr<uchar> ( i );
                for ( int j = 0; j < img_width; j++ ) {
                    int value = img_data[j];
                    Point2i value_pos;
                    value_pos.x = j;
                    value_pos.y = i;
                    infos[value].push_back ( value_pos );
                }
            }
            QMap<int, vector<Point2i>>::Iterator i = infos.begin();

            QVector<double> draw_index;
            QVector<double> draw_value;

            while ( i!= infos.end() ) {
                draw_index.push_back ( i.key() );
                draw_value.push_back ( i.value().size() );

                ++i;
            }

            draw_line ( draw_index, draw_value );


        }




    }
}
