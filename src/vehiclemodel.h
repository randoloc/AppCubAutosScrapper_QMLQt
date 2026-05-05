#ifndef VEHICLEMODEL_H
#define VEHICLEMODEL_H

#include <QAbstractListModel>
#include <QJsonObject>
#include <QJsonArray>
#include <QString>
#include <QVariant>

class VehicleModel : public QAbstractListModel
{
    Q_OBJECT

public:
    enum Roles {
        TitleRole = Qt::UserRole + 1,
        PriceRole,
        CurrencyRole,
        SourceLabelRole,
        SourceRole,
        UrlRole,
        ProvinceRole,
        MunicipalityRole,
        ContactNameRole,
        ContactPhoneRole,
        ContactWhatsappRole,
        DescriptionRole,
        AutonomiaKmRole,
        ModeloRole,
        BatteryKwhRole,
        ChargingTimeRole,
        ImagesRole,
        ImageUrlRole
    };

    VehicleModel(QObject *parent = nullptr);

    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;
    QHash<int, QByteArray> roleNames() const override;

    Q_INVOKABLE void clear();
    Q_INVOKABLE QString getImagesAsJson(int index) const;
    Q_INVOKABLE int count() const { return rowCount(); }
    Q_INVOKABLE QVariantMap get(int index) const;

    void loadFromJson(const QJsonArray &array);

private:
    struct Vehicle {
        QString title;
        double price;
        QString currency;
        QString sourceLabel;
        QString source;
        QString url;
        QString province;
        QString municipality;
        QString contactName;
        QString contactPhone;
        QString contactWhatsapp;
        QString description;
        int autonomiaKm;
        QString modelo;
        double batteryKwh;
        QString chargingTime;
        QStringList images;
        QString primaryImage;
    };

    QList<Vehicle> m_vehicles;
};

#endif
